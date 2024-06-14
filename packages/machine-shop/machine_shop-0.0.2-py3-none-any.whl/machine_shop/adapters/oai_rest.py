# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ..util.xml_tags import extract_xml_tagged_content


def prepared_oai_messages(input):
    """
    :input_format
        messages = [
            {"role": "world",   "name": "openai",   "content": "Be an Abstract Intellect."},
            {"role": "human",   "name": "alex",     "content": "Can we discuss this?"},
            {"role": "machine", "name": "chatgpt",  "content": "Yes."}
            {"role": "human",   "name": "alex",     "content": "Then let's do it."}
        ]
    :outputformat
        messages = [
            {"role": "system",      "content": "Be an Abstract Intellect."}
            {"role": "user",        "content": "Can we discuss this?"}
            {"role": "assistant",   "content": "Yes."}
            {"role": "user",        "content": "Then let's do it."}
        ]
    """
    output_messages = []
    for message in input:
        output_message = {}
        if message['role'] == 'human':
            output_message['role'] = 'user'
        elif message['role'] == 'machine':
            output_message['role'] = 'assistant'
        elif message['role'] == 'world':
            output_message['role'] = 'system'
        output_message['content'] = message['content']
        output_messages.append(output_message)
    return input, output_messages


def formatted_oai_message(output):
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
    if output['role'] == 'assistant':
        formatted_output['role'] = 'machine'
        formatted_output['name'] = 'chatgpt'
        txt, tags = extract_xml_tagged_content(
            output['content'],
            placeholders=True # default for now delete if not needed.
        )
        formatted_output['content'] = txt
        if len(tags) > 0:
            formatted_output['tags'] = tags
    else:
        print('The role is not assistant')
    return formatted_output


def format_oai_output(output):
    """
    :list of choices
    :return: formatted_output, other
    """
    solo_candidate = output['choices'].pop(0)
    formatted_output = formatted_oai_message(solo_candidate['message'])
    if len(output['choices']) > 0:
        other = []
        for choice in output['choices']:
            other_formatted = formatted_oai_message(choice['message'])
            other.append(other_formatted)
    else:
        other = None
    return formatted_output, other
