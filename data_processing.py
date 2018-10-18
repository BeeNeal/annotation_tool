import json
from pprint import pprint

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


def process_annotated_text(annotated_line, color_slots_obj):
    """Takes highlighted text from JS, removes font tags, and adds slot tags"""

    colors_to_slots = json.loads(color_slots_obj)
    print(colors_to_slots)
    # will be returning slotted text line 
    return "These routes are working"


# dict we're dealing with:
# {'["acmodel"': '#FF4E00', ' "acmodelnumber"': '#8EA604', ' "actype"]': '#F5BB00'}
# Ugh. It's come to it. No point spending time processing the slot tags excess [] 
# and "" when needs to be done farther up the line in JS











