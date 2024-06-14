# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ..util.xml_tags import extract_xml_tagged_content


def prepared_plm_prompt(input):
    prompt = {
        "text":f"{input[0]['content']}"
    }
    return input, prompt


def formatted_plm_message(output):
    """
    :input_format
        messages = [
            {"role": "assistant",   "content": "I will lay it out later"}
        ]
    :outputformat
        messages = [
            {"role": "machine", "name": "chatgpt",   "content": "I will lay it out later"}
        ]
    """
    formatted_output = {}
    formatted_output['role'] = 'machine'
    formatted_output['name'] = 'palm'
    txt, tags = extract_xml_tagged_content(
        output,
        placeholders=True # default for now delete if not needed.
    )
    formatted_output['content'] = txt
    if len(tags) > 0:
        formatted_output['tags'] = tags
    return formatted_output


def format_plm_output(output):
    """
    :list of choices
    :return: formatted_output, other
    """
    solo_candidate = output['candidates'].pop(0)
    formatted_output = formatted_plm_message(solo_candidate['output'])
    if len(output['candidates']) > 0:
        other = []
        for choice in output['candidates']:
            other_formatted = formatted_plm_message(choice['output'])
            other.append(other_formatted)
    else:
        other = None
    return formatted_output, other
