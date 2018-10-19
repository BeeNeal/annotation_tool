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


def extract_slot_colors(annotated_line):
    """Extract slot color codes by index"""

    ordered = []

    for color in list(sample_dict.values()):
        color_index = sample_text.index(color)
        ordered.append(sample_text[color_index: color_index + 7])

    return ordered


def replace_font_with_slot(annotated_line, ordered_slots):
    """Inserts slot name at ending font tags"""

    new_line = annotated_line

    # need to do recursively, b/c strings immutable and don't change in place, 
    # so need to keep running function on same line of text
    while '</font>' in new_line:
        new_line = new_line.replace('</font>', ordered_slots.pop(0), 1)
        return replace_font_with_slot(new_line, ordered_slots)

    return new_line



def process_annotated_text(annotated_line, color_slots_obj):
    """Takes highlighted text from JS, removes font tags, and adds slot tags"""

    colors_to_slots = json.loads(color_slots_obj)
    ordered_slots = extract_slot_colors(annotated_line)
    
    # will be returning slotted text line 
    return "These routes are working"


# dict we're dealing with:
sample_text = """ "qa__ac_enhancement   <font color="#ff4e00">What</font> is the 
<font color="#8ea604">best</font> way to use <font color="#f5bb00">enhancement mode</font>?" """

sample_dict = {'["acmodel"': '#ff4e00', ' "acmodelnumber"': '#8ea604', ' "actype"]': '#f5bb00'}
# Ugh. It's come to it. No point spending time processing the slot tags excess [] 
# and "" when needs to be done farther up the line in JS


#  what if I replaced the fontcolor code with the actual slot name? Then would just have to take out the trash!
# but strings are immutable...
# want:
# "qa__ac_enhancement|<["acmodel"> What is the best|< "acmodelnumber"> way to use enhancement|< " "actype\"]"> mode|< " "actype"]\">?"

# the font will consistently be <> wrapped
# take text until </

# use a stack to collect the font color, and slot accordingly

# could use regex to collect font colors in order
# then could split on </font>
# all text starting with > (front the font color tag) is text that needs to be slotted

# for i in range(len(annotated_line)):
#     pass



# don't need to make another dict, just need to add on |< SLOT > - although if adding on the tail > is complicated
# perhaps should make another dict









