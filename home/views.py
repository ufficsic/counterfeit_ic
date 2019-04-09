from counterfeit_ic import app, mail
from flask import url_for, render_template
from flask_mail import Message
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('index.html')

@app.route('/edit')
def edit():
    return render_template('index.html')
