from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import helper_functions

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

FNAMES = helper_functions.ls_files()



@app.route('/', methods=['GET'])
def index():
    """Routes to login if no username in session."""

    if 'username' in session and session['username']:
        user = session['username']
        return render_template("annotation_tool.html", user=user, fnames=FNAMES)
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
        # return render_template("annotate_content.html", fname=file, content=content )


@app.route('/pewpew', methods=['POST'])
def pewpew():
    """test route"""

    x = "PEW PEW PEW PEW PEW"
    print(x)
    return jsonify(x)

# FAKE ROUTE FOR TEST PURPOSES
@app.route('/test', methods=['POST'])
def collect_fname():
    file_name = request.form.get('title')
    print(file_name)

    return render_template("show_file.html", user=session['username'],
                                             fileName=file_name )



@app.route('/annotation_tool/<title>', methods=["POST"])
def display_file(title):
    """Displays file line by line after retrieving file name."""

    # AJAX call
    file_name = request.form.get('title')
    print ('heyo', file_name)
    fnames = helper_functions.ls_files()
    print(file_name)

    return render_template("annotation_tool.html", user=session['username'],
                                                   fnames=fnames, )


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
