from counterfeit_ic import app
from flask import render_template


@app.route('/taxonomy')
def taxonomy():
    return render_template('taxonomy/taxonomy.html')