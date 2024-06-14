# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ..util.xml_tags import extract_xml_tagged_content


def prepared_gem_messages(input):
    """
    :input_format
        messages = [
            {"role": "human",   "name": "alex",     "content": "Can we discuss this?"},
            {"role": "machine", "name": "gemini",   "content": "Yes."}
            {"role": "human",   "name": "alex",     "content": "Then let's do it."}
        ]
    :outputformat
        messages = [
            {"role":"user", "parts":[{"text": "Can we discuss this?"}]},
            {"role":"model", "parts":[{"text": "Yes."}]},
            {"role":"user", "parts":[{"text": "Then let's do it."}]}
        ]
    """
    prepared_output = []
    for message in input:
        output_message = {}
        if message['role'] == 'human':
            output_message['role'] = 'user'
        elif message['role'] == 'machine':
            output_message['role'] = 'model'
        output_message['parts'] = [{'text': message['content']}]
        prepared_output.append(output_message)
    return input, prepared_output


def formatted_gem_output(output):
    """
    :param output a dictionary returned from gemini_rest
    :return: formatted_output
    """
    solo_candidate = output['candidates'][0]['content']
    text = ''
    for part in solo_candidate['parts']:
        text += part['text'] + ' '
    formatted_output = {}
    if solo_candidate['role'] == 'model':
        formatted_output['role'] = 'machine'
        formatted_output['name'] = 'gemini'
        txt, tags = extract_xml_tagged_content(
            text,
            placeholders=True  # default for now delete if not needed.
        )
        formatted_output['content'] = txt
        if len(tags) > 0:
            formatted_output['tags'] = tags
    else:
        print('The role is not model')
    return formatted_output
