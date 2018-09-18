from flask import (Flask, jsonify, render_template, redirect, request,
                   flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "ABC"



@app.route('/', methods=['GET'])
def index():
    """Routes to login if no username in session."""

    if 'username' in session and session['username']:
        user = session['username']
        return render_template("annotation_tool.html", user=user)
    else:
        return render_template("login.html")


@app.route('/annotation_tool', methods=['POST'])
def annotation_tool():
    """Grabs username and routes to annotation tool page"""

    user = request.form.get('username')
    if user is None:
        return render_template("login.html")
    session['username'] = user

    return render_template("annotation_tool.html", user=user)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads"
    # our web app if we change the code.
    app.run(debug=True)
