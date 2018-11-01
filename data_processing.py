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

        #  need to make it so does not error out when no slots
    slot_options = data[label].get('slots')
    if slot_options:
        slots = list(slot_options)
        return slots
    else:
        return None

# # # # # # # # # # Above this processes file data# # # # # # # # # # # # # # #
 

def all_indices(annotated_line, sub):
    """Extracts all starting indices of color codes, returns list of indices"""

    indices = []
    for match in re.finditer(sub, annotated_line):
        color_code_index = match.start()
        indices.append(color_code_index)

    return indices


def extract_slot_colors(annotated_line, colors_to_slots):
    """Returns an list of the slot names in order of how were highlighted"""

    colors_to_slots = json.loads(colors_to_slots)
    ordered_slots = []
    indices = all_indices(annotated_line, '<font color=')

    for i in indices:
        color_code = annotated_line[i+13:i+20]
        ordered_slots.append(colors_to_slots[color_code])

    return ordered_slots


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

    completely_tagged = ''

    for item in text_with_slots:
        if "|<" in item:
            completely_tagged += tag_when_spaces(item)
        else:
            completely_tagged += item

    return completely_tagged


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

    # remove remnants of the opening font tag, ie:'"#8ea604">'
    new_item[0] = new_item[0][10:]
    return ' '.join(new_item)


def process_annotated_text(annotated_line, color_slots_obj):
    """Takes highlighted text from JS, removes font tags, and adds slot tags"""

    colors_to_slots = color_slots_obj
    first_pass = replace_font_with_slot(annotated_line, colors_to_slots)
    tagged_text = tag_all_words(first_pass)

    return tagged_text


# # # # # # # # # # Below this writes data to new file # # # # # # # # # # # # #


def append_file_text(annotated_pkg, file_name, username):
    """Takes in annotated text, writes to new file labeled with username"""

    print(annotated_pkg + file_name + username)

    file_name_wo_ext = file_name[:-4]
    new_file = file_name_wo_ext + '_' + username + '.txt'
    f = open(new_file, 'a+')
    f.write(annotated_pkg + '\n')
    f.close()

    return




