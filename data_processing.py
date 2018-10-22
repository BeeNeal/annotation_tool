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
 

def extract_slot_colors(annotated_line):
    """Extract slot color codes by index"""

    ordered = []

    for color in list(sample_dict.values()):
        color_index = sample_text.index(color)
        ordered.append(sample_text[color_index: color_index + 7])

    return ordered


def replace_font_with_slot(annotated_line, ordered_slots, colors_to_slots):
    """Inserts slot name at ending font tags"""

    new_line = annotated_line

    if '</font>' in new_line:
        new_line = new_line.replace('</font>', ('|<' + colors_to_slots[ordered_slots.pop(0)]) + '>', 1)
        return replace_font_with_slot(new_line, ordered_slots, colors_to_slots)

    return new_line

def second_pass(new_line):
    """ """

    print(new_line.split("<font color="))
    return new_line.split("<font color=")


def process_annotated_text(annotated_line, color_slots_obj):
    """Takes highlighted text from JS, removes font tags, and adds slot tags"""

    colors_to_slots = json.loads(color_slots_obj)
    ordered_slots = extract_slot_colors(annotated_line)
    first_pass = replace_font_with_slot(annotated_line, ordered_slots, 
                                        colors_to_slots)
    print(second_pass(first_pass))
    # will be returning slotted text line 
    return "These routes are working"


# dict we're dealing with:
sample_text = """ "qa__ac_enhancement   <font color="#ff4e00">What</font> is the 
<font color="#8ea604">best</font> way to use <font color="#f5bb00">enhancement mode</font>?" """

processed_once = """ "qa__ac_enhancement   <font color="#ff4e00">WhatTHIS is the 
<font color="#8ea604">best**** way to use <font color="#f5bb00">enhancement mode#####?" """

sample_dict = {'["acmodel"': '#ff4e00', ' "acmodelnumber"': '#8ea604', ' "actype"]': '#f5bb00'}
# Ugh. It's come to it. No point spending time processing the slot tags excess [] 
# and "" when needs to be done farther up the line in JS


# want:
# "qa__ac_enhancement|<["acmodel"> What is the best|< "acmodelnumber"> way to use enhancement|< " "actype\"]"> mode|< " "actype"]\">?"

# the font will consistently be <> wrapped
# take text until </

# use a stack to collect the font color, and slot accordingly



['',
 '"#ff4e00">qa__ac_enhancement|<["acmodel"> What is the ', 
'"#8ea604">best|< "acmodelnumber"> way to use ',
 '"#f5bb00">example enhancement|< "actype"]> mode?\n']

def second_pass(text_with_slots):
    """Takes in text with font tags replaced by slot; tags remaining words."""
    
    seen_tag_opener = False
    seen_pipe = False
    seen_space = False
    word_span = 0
    second_pass = ''

    for item in lst:
        for i in range(len(item)):
            if item[i] == '|' and not seen_space:
                second_pass += item
                continue
            elif item[i] == '|' and seen_space:
                second_pass += process_space(item)
                continue
            elif item[i] == '>':
                seen_tag_opener = True
            elif item[i] == ' ':
                seen_space = True


def process_space(item):
    """Slot annotation for 2+ consec words are annotated with same slot."""

    # finds the slot of the item
    slot_start = item.index('|<')
    slot_end = item.index('>', slot_start)
    slot_tag = item[slot_start:slot_end + 1]

#  could do it this way, but then would have to run it again in case 3 words tagged with same slot
    tag_start = item.index('>')
    space_index = item.index(' ', tag_start, slot_start)


    new_item = ''
    seen_pipe = False
    seen_tag_opener = False

#  can try it this way, but would be easier to turn into a list, use contains, then join back together?
    for char in item:
        if char == '>':
            seen_tag_opener = True
        elif char == ' ':
            if seen_tag_opener = True:
                new_item += item[]

        new_item += char

def proc(item):

    slot_start = item.index('|<')
    slot_end = item.index('>', slot_start)
    slot_tag = item[slot_start:slot_end + 1]

    new_item = item.split(" ")
    for i in range(len(new_item)):

        if '|<' in new_item[i]:
            break
        else:
            new_item[i] = str(new_item[i]) + slot_tag + ' '

    return ''.join(new_item)


 '"#f5bb00">example enhancement|< "actype"]> mode?\n'
 ['"#f5bb00">example', 'enhancement|<', '"actype"]>', 'mode?\n']








    # OK, by having the chunks split on <font> know that there is only one annotation per chunk
    # so even though forces us to get n2 runtime instead of greedy, OK b/c small lines, and less room for error

    # need to create state of if in font bracket tags and if not tagged/more than one word between tags


# third_pass will be complete line, of font trash taken out and dooone!

# What we have now is complete EXCEPT for when 2 words occur in same slot tag, and are tagged with same slot
# need to see '>' and space without pipe


















