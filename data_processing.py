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

    return list(data[label].get('slots').keys())
