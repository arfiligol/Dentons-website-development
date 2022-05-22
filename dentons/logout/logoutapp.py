from flask import Blueprint, redirect, url_for, session

Logout_blueprints = Blueprint('Logout', __name__)

@Logout_blueprints.route('/')
def logout():
    # delete session config
    session['loggedin'] = False
    session['id'] = None
    session['username'] = None
    session['account_level'] = None

    # Redirect to login page
    return redirect(url_for('Login.login'))