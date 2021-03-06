from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from model_addition import *
import helper_functions, data_processing, db_helpers
import json

# keep below chunk in model file
from flask import Flask
app = Flask(__name__)


# toolbar = DebugToolbarExtension(app)
# secret key for the session
app.secret_key = 'abc'

app.jinja_env.undefined = StrictUndefined

# FIXME - make FNAMES come from DB (Dataset, text?) instead of directories
FNAMES = helper_functions.ls_files()

# FIXME - Don't actually need labels - these will come connected to dataset text
LABELS = data_processing.labels_from_json('/Users/bneal/Desktop/annotation_tool/data_files/annotation_structure.json')


# FIXME - change to getting annotator id from session from DB
@app.route('/', methods=['GET'])
def index():
    """Routes to login if no username in session, or annotool if logged in."""

    if 'username' in session and session['username']:
        user = session['username']
        return render_template("annotation_tool.html", user=user, fnames=FNAMES,
                                                       labels=LABELS)
    else:
        return render_template("login.html")


@app.route('/annotation_tool', methods=['POST'])  # must be post b/c updating session
def annotation_tool():
    """Grabs username and routes to annotation tool page"""

    # make sure user is logged in, if not, render login template
    user = request.form.get('username')
    if user is None:
        return render_template("login.html")

    session['username'] = user

    return render_template('annotation_tool.html', user=user,
                                                   fnames=FNAMES,
                                                   labels=LABELS
                                                   )

# change to selecting a dataset/task
@app.route('/annotate_content', methods=['POST'])
def display_content():
    """Returns jsonified text content of selected file."""

    file_name = request.form.get('title')
    if file_name:
        content = helper_functions.return_text(file_name)
    else:
        content = 'Please select a file'
  
    return jsonify(content)


@app.route('/generate_slots', methods=['POST'])
def generate_slots():
    """Returns slot options for selected label"""

    label = request.form.get('label')
    slots = data_processing.slots_from_labels(label[1:])

    return json.dumps(slots)


# for annotated text processing 
@app.route('/process_text', methods=['POST'])
def process_annotated_text():
    """Grab highlighted text from JS, returns text with tags"""

    annotated_line = request.form.get('text')
    colors_to_slots = request.form.get('colorSlotsObj')
    # entities = request.form.get('entities')
    start_indices = request.form.get('start_indices')
    end_indices = request.form.get('end_indices')

    ordered_slots = data_processing.extract_slot_colors(annotated_line, 
                                                        colors_to_slots)

    db_helpers.add_entities_to_db(json.loads(start_indices), 
                                  json.loads(end_indices),
                                  ordered_slots)

    annotated_text = data_processing.process_annotated_text(annotated_line, 
                                                            colors_to_slots)

    return jsonify(annotated_text)


@app.route('/write_to_file', methods=['POST'])
def append_to_file():
    """Receive post req with annotated line, append it to new file"""

    annotated_pkg = request.form.get('annotated')
    file_name = request.form.get('fileName')
    username = session['username']
    data_processing.append_file_text(annotated_pkg, file_name, username)

    # return next line for processing
    return annotated_pkg

# HERE TO ADD ENTITIES TO DB ONCE ANNOTATED

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    # app.debug = True
    connect_to_db(app)
    app.config['SECRET_KEY'] = 'SUPERSECRETKEY'
    app.run(port=5000, host='0.0.0.0')
