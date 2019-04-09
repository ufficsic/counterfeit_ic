from counterfeit_ic import app
from flask import render_template

@app.route('/instructions')
def instructions():
    return render_template('instructions/instructions.html')