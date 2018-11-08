from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import helper_functions, data_processing
import json

app = Flask(__name__)
toolbar = DebugToolbarExtension(app)
# secret key for the session
app.secret_key = 'abc'

app.jinja_env.undefined = StrictUndefined

FNAMES = helper_functions.ls_files()
LABELS = data_processing.labels_from_json('/Users/bneal/Desktop/annotation_tool/data_files/annotation_structure.json')


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


@app.route('/annotate_content', methods=['POST'])
def display_content():
    """Returns jsonified text content of selected file."""

    file_name = request.form.get('title')
    if file_name:
        content = helper_functions.return_text(file_name)
    else:
        content = 'woohoo'
  
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

    # Try changing all oxf this to GET instead of POST when get a chance
    annotated_line = request.form.get('text')
    colors_to_slots = request.form.get("colorSlotsObj")
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


# Fake route for test purposes
@app.route('/pewpew', methods=['POST'])
def pewpew():
    """test route"""

    x = "PEW PEW PEW PEW PEW"
    print(x)
    return jsonify(x)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
    # app.debug = True
    app.config['SECRET_KEY'] = 'SUPERSECRETKEY'
