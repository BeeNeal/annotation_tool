from data_processing import labels_from_json, slots_from_labels
from model_addition import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

file = '/Users/bneal/Desktop/annotation_tool/data_files/annotation_structure.json'

def seed_intent_labels():
    """ """
    intent_labels = labels_from_json(file)

    for label in intent_labels:
        # new_label = IntentLabel(label)
        db.session.add(IntentLabel(intent_label=label))

    db.session.commit()


def slots_from_labels(label):
    """Takes in label and reads JSON file to return slot options"""

    with open(file, encoding='utf-8') as f:
        data = json.loads(f.read())

        #  need to make it so does not error out when no slots
    slot_options = data[label].get('slots')
    if slot_options:
        slots = list(slot_options)
        for slot in slots:
            db.session.add(EntityLabel(entity_label=slot, intent_label=label))
        db.session.commit()
    else:
        return None


def seed_entities_with_json_labels():
    """ """
    intent_labels = labels_from_json(file)

    for label in intent_labels:
        entity_labels = slots_from_labels(label)

    db.session.commit()
 
# seed_intent_labels()
# seed_entities_with_json_labels()


# select all entity_labels where intent_label == qa__ac_introduction
