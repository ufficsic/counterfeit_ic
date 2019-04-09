from counterfeit_ic import app, db, archives
from flask import render_template, redirect, session, Response, request, url_for, flash, abort
from dataset.models import Dataset
from user.models import User
from werkzeug import secure_filename
from dataset.forms import UploadForm
from user.decorators import login_required, approval_required, admin_required
import logging
import time


@app.route('/dataset', methods=('GET', 'POST'))
@approval_required
def dataset():
    form = UploadForm()
    user_id = session.get('id')
    user = User.query.filter_by(
        id=user_id,
    ).first()
    if (request.method == 'POST'):
        if form.validate_on_submit() and 'archive' in request.files:
            for archived_file in request.files.getlist('archive'):
                filename = archives.save(archived_file)
                logging.info(filename)
                print('request.files ', filename)
                dataset = Dataset(
                    name=form.name.data,
                    description=form.description.data,
                    filename=filename,
                    user_id=user_id,
                )
                try:
                    db.session.add(dataset)
                    db.session.commit()
                    flash('Dataset uploaded successfully!', 'success')
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    error = 'Error Uploading the file.'
                    flash(error, 'error')
        else:
            error = 'Invalid File, ZIP and RAR Files only!'
            flash(error, 'error')
    files = Dataset.query.all()
    return render_template('dataset/dataset.html', files=files, archives=archives, form=form, user=user)


@app.route('/dataset/delete', methods=('POST',))
@approval_required
def delete_dataset():
    if (request.method == 'POST'):
        archive_ids = request.form.getlist('archive_id')
        for id in archive_ids:
            dataset = Dataset.query.filter_by(
                id=id
            ).first()
            if (dataset.user == session.get('id') or session.get('is_admin')):
                db.session.delete(dataset)
        db.session.commit()
    return redirect(url_for('dataset'))
