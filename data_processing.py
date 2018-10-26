import json
import re

file = '/Users/bneal/Desktop/annotation_tool/data_files/annotation_structure.json'



def labels_from_json(file):
    """Takes in a JSON file, and returns keys"""

    with open(file, encoding='utf-8') as f:
        data = json.loads(f.read())

    return data.keys()


def slots_from_labels(label):
    """Takes in label and reads JSON file to return slot options"""

    with open(file, encoding='utf-8') as f:
        data = json.loads(f.read())

        #  need to make it so does no error out when no slots
    slot_options = data[label].get('slots')
    if slot_options:
        slots = list(slot_options)
        return slots
    else:
        return None

# # # # # # # # # # Above this processes file data# # # # # # # # # # # # # # #
 

def extract_slot_colors(annotated_line, colors_to_slots):
    """Return list of slots in order of annotation"""

    ordered = []

    # in this loop, finding all the indices of #colorcodes in the annotated line, and extract them
    # need colors_to_slots to be slot:#colorcode format
    # INSTEAD, return ordered SLOTs and do the lookup conversionhere instead of in the font replace funct

    # Loop over color codes and match them(find index of and extract) with what's in string, preserving the order
    colors_to_slots = json.loads(colors_to_slots)

    for color in list(colors_to_slots.keys()):
        color_index = annotated_line.index(color)
        color_code = annotated_line[color_index: color_index + 7]
        # should now have ordered SLOTS instead of ordered color code
        ordered.append(colors_to_slots[color_code])
    print(ordered)

    return ordered


sample_text = """ "qa__ac_enhancement   <font color="#ff4e00">What</font> is the 
<font color="#8ea604">best</font> way to use <font color="#f5bb00">enhancement mode</font>?" """

processed_once = """ "qa__ac_enhancement   <font color="#ff4e00">WhatTHIS is the 
<font color="#8ea604">best**** way to use <font color="#f5bb00">enhancement mode#####?" """

sample_dict = {'["acmodel"': '#ff4e00', ' "acmodelnumber"': '#8ea604', ' "actype"]': '#f5bb00'}


# def replace_font_with_slot(annotated_line, colors_to_slots):
#     """Inserts slot name at ending font tags - returns list"""
#
#     ordered_slots = extract_slot_colors(annotated_line, colors_to_slots)
#     new_line = annotated_line
#
#     if '</font>' in new_line:
#         current_slot = ordered_slots.pop(0)
#         print(current_slot)
#         new_line = new_line.replace('</font>', ('|<' + current_slot) + '>', 1)
#         return replace_font_with_slot(new_line, colors_to_slots)
#
#     return new_line.split("<font color=")


def replace_font_with_slot(annotated_line, colors_to_slots):
    """Inserts slot name at ending font tags - returns list"""

    ordered_slots = extract_slot_colors(annotated_line, colors_to_slots)
    new_line = annotated_line
    while '</font>' in new_line:
        current_slot = ordered_slots.pop(0)
        new_line = new_line.replace('</font>', ('|<' + current_slot + '>'), 1)

    return new_line.split("<font color=")


def tag_all_words(text_with_slots):
    """Takes in list of font-tags-replaced-by-slot text; tags remaining words"""

    second_pass = ''

    for item in text_with_slots:
        if "|<" in item:
            second_pass += tag_when_spaces(item)
        else:
            second_pass += item

    return second_pass


def extract_slot_from_line(item):
    """Slot annotation for 2+ consec words are annotated with same slot."""

    # finds the slot of the item
    slot_start = item.index('|<')
    slot_end = item.index('>', slot_start)
    slot_tag = item[slot_start:slot_end + 1]

    return slot_tag


def tag_when_spaces(item):
    """Takes in space separated words, tags all of them with slot tag."""

    slot_tag = extract_slot_from_line(item)

    new_item = item.split(" ")
    for i in range(len(new_item)):

        if '|<' in new_item[i]:
            break
        else:
            new_item[i] = str(new_item[i]) + slot_tag + ' '

    new_item[0] = new_item[0][10:]
    return ' '.join(new_item)


def process_annotated_text(annotated_line, color_slots_obj):
    """Takes highlighted text from JS, removes font tags, and adds slot tags"""

    # colors_to_slots = json.loads(color_slots_obj)
    colors_to_slots = color_slots_obj
    # ordered_slots = extract_slot_colors(annotated_line, colors_to_slots)
    first_pass = replace_font_with_slot(annotated_line, colors_to_slots)

    tagged_text = tag_all_words(first_pass)

    return tagged_text




