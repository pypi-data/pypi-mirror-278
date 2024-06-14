# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import xml.etree.ElementTree as ElementTree


HUMAN_PREFIX        = "\n\nHuman:"
MACHINE_PREFIX      = "\n\nAssistant:"


# The firmware code. But you need to know the tag names and if they are not closed... boom!
# def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
#     ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
#     if strip:
#         ext_list = [e.strip() for e in ext_list]
#     return ext_list

def extract_xml_tagged_content(text, placeholders: bool = False) -> (str, list[dict]):
    """ If you uncommentremoves all the multilevelled tags.
    Then flattens the text with the tag placeholders instead of the tags.\
    The problem is, that together with the multilevelled tags, it remove
    the text that is _after_ it. So, this is not a solution, only the re.
    """
    message = f'<message>{text}</message>'
    message_as_root = ElementTree.fromstring(message)

    # may_be = True
    # multilevelled = []
    # while may_be:
    #     may_be = False
    #     next_level = next(message_as_root.iter())
    #     for child in next_level:
    #         if len(child) > 0:
    #             about_to_remove = deepcopy(child)
    #             multilevelled.append(about_to_remove)
    #             next_level.remove(child)
    #             may_be = True  # removed one, so we're proably not done.
    #     # if no grandchildren at all, we're done
    #
    # Now we have the removed multilevelled tags in a list,
    # I'm not going to process them now; it requires a separate function. Later.
    #
    # Commented out for now, because it drops the text that is _after_ the tags.

    # Flatten the text
    txt = ''.join(
        message_as_root.itertext()  # flattened text without tags (text within the tags included).
    )
    next_level = next(message_as_root.iter())
    tags = []
    for child in next_level:
        tag = child.tag
        text = child.text
        if placeholders:
            place_holder = f"({tag})"
        else:
            place_holder = ''
        txt = txt.replace(text, place_holder)  # remove the text from the tags
        tags.append({tag: text})  # store the content of the tags
    return txt, tags
