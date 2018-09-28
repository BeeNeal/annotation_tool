from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import helper_functions, data_processing

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

FNAMES = helper_functions.ls_files()
LABELS = data_processing.labels_from_json('/Users/bneal/Desktop/annotation_tool/data_files/annotation_structure.json')

@app.route('/', methods=['GET'])
def index():
    """Routes to login if no username in session."""

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

    # this route should probs just be a login route

    return render_template('annotation_tool.html', user=user, 
                                                   fnames=FNAMES,
                                                   labels=LABELS
                                                   )


@app.route('/annotate_content', methods=['POST'])
def display_content():
    """ """

    file_name = request.form.get('title')
    if file_name:
        content = helper_functions.return_text(file_name)
    else:
        content = 'woohoo'
  
    return jsonify(content)


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
    # debug=True gives us error messages in the browser and also "reloads"
    # our web app if we change the code.
    app.run(debug=True)
    app.debug = True
    toolbar = DebugToolbarExtension(app)
