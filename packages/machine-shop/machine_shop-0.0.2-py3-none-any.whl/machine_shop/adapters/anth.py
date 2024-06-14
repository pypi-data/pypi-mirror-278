# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ..util.xml_tags import extract_xml_tagged_content


HUMAN_PREFIX = "\n\nHuman:"
MACHINE_PREFIX = "\n\nAssistant:"


def prepared_ant_messages(input):
    """
    :input_format
        messages = [
            {"role": "human", "name": "alex", "content": "Can we discuss this?"},
            {"role": "machine", "name": "claude", "content": "Yes."}
            {"role": "human", "name": "alex",     "content": "Then let's do it."}
        ]
    :outputformat
        messages = [
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
        output_message['content'] = message['content']
        output_messages.append(output_message)
    return input, output_messages


def formatted_ant_output(output):
    """
    :input_format
        messages = [
            {"role": "assistant",   "content": "I will lay it out later"}
        ]
    :outputformat
        messages = [
            {"role": "machine", "name": "claude",
            "content": "I will lay it out later",
            "tags":[]}  # tags are optional and can be absent.
        ]
    """
    formatted_output = {}
    if output['role'] == 'assistant':
        formatted_output['role'] = 'machine'
        formatted_output['name'] = 'claude'
        txt, tags = extract_xml_tagged_content(
            output['content'][0]['text'],
            placeholders=True # default for now delete if not needed.
        )
        formatted_output['content'] = txt
        if len(tags) > 0:
            formatted_output['tags'] = tags
    else:
        print('The role is not assistant')
    return formatted_output


def prepared_ant_prompt(input):
    """
    :input_format
        messages = [
            {"role": "human",   "name": "alex",     "content": "Can we discuss this?"}
        ]
    :output_format
        prompt = "\n\nHuman: Can we discuss this?"
    """
    output = f"{HUMAN_PREFIX} {input[0]['content']}{MACHINE_PREFIX} "
    return input, output


def formatted_ant_completion(output):
    """
    :input_format
        completion = "Yes.
    :output_format
        messages = [
            {"role": "machine", "name": "claude",
            "content": "I will lay it out later",
            "tags":[]}  # tags are optional and can be absent.
        ]
    """
    formatted_output = {}
    formatted_output['role'] = 'machine'
    formatted_output['name'] = 'claude'
    txt, tags = extract_xml_tagged_content(
        output['completion'],
        placeholders=True  # default for now delete if not needed.
    )
    formatted_output['content'] = txt
    if len(tags) > 0:
        formatted_output['tags'] = tags
    return formatted_output
