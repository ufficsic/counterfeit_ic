from counterfeit_ic import app
from flask import render_template


@app.route('/resources')
def resources():
    return render_template('resources/resource.html')