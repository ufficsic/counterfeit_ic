from counterfeit_ic import app
from flask import render_template

@app.route('/contact')
def contact():
    app.logger.info('test')
    return render_template('contact/contact.html')
