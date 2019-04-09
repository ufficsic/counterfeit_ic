from counterfeit_ic import app, db, mail
from flask_mail import Message
from flask import render_template, redirect, session, request, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_
from user.forms import RegisterForm, LoginForm, ForgotForm, PasswordResetForm
from user.models import User
from user.decorators import login_required, approval_required, admin_required
from user.decorators import login_required, admin_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully!', 'success')
            flash(
                'Please contact the admin to be be approve your account to login!', 'success')
            flash('Admin info is found in the Contact tab!', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('User already exists!', 'error')
    return render_template('user/register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(
            func.lower(User.username) == form.username.data).first()
        if user:
            if not user.is_approved:
                flash('Account is not approved yet!', 'error')
                flash(
                    'Please contact the admin to be be approve your account to login!', 'error')
                flash('Admin info is found in the Contact tab!', 'error')
                return render_template('user/login.html', form=form)
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                login_user(user)
                session['username'] = user.username
                session['id'] = user.id
                session['is_admin'] = user.is_admin
                session['is_approved'] = user.is_approved
                session['is_contributor'] = user.is_contributor

                return redirect(request.args.get('next') or url_for('index'))
            else:
                error = 'Incorrect username or password'
                flash(error, 'error')
        else:
            error = 'Incorrect username or password'
            flash(error, 'error')
    return render_template('user/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    if session.get('username'):
        session.pop('username')
        session.pop('id')
        session.pop('is_admin')
        session.pop('is_contributor')
        session.pop('is_approved')
    logout_user()
    return redirect(url_for('index'))


@app.route('/password-reset', methods=('GET', 'POST'))
def password_reset():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data.lower(),
        ).first()
        if user:
            expire_in_twenty_four_hours = 24*3600
            serial = Serializer(
                app.config['SECRET_KEY'], expires_in=expire_in_twenty_four_hours)
            code = serial.dumps({'id': user.id}).decode('utf-8')
            # send email here
            body_html = render_template(
                'mail/user/password_reset.html', code=code, name=user.fullname)
            msg = Message(
                subject='{fullname}, here\'s the link to reset your counterfeit-ic password'.format(
                    fullname=user.fullname),
                html=body_html,
                recipients=[user.email]
            )
            mail.send(msg)
            flash('Email has been sent with link to password reset!', 'success')
        else:
            error = 'Invalid email. Please try again.'
            flash(error, 'error')
    return render_template('user/password_reset_request.html', form=form)


@app.route('/reset-password/<code>', methods=('GET', 'POST'))
def reset_password(code):
    serial = Serializer(app.config['SECRET_KEY'])
    user_obj = None
    form = PasswordResetForm()
    require_current = None
    error = None
    if request.method == 'POST':
        del form.current_password
        if form.validate_on_submit():
            try:
                user_obj = serial.loads(code)
            except Exception as e:
                error = 'Invalid or expired password reset link. Please reset your password again.'
                flash(error, 'error')
                return redirect(url_for('login'))
                # return render_template('error.html')

            user = User.query.filter_by(
                id=user_obj['id'],
            ).first()

            if not user:
                error = 'User does not exist. Please try again with a valid email.'
                flash(error, 'error')
                return redirect(url_for('login'))

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.password.data, salt)
            user.password = hashed_password
            # user.save()
            db.session.add(user)
            db.session.commit()
            if session.get('username'):
                session.pop('username')
            return render_template('user/reset_password_confirm.html')

    return render_template('user/reset_password.html',
                           form=form,
                           error=error,
                           require_current=require_current,
                           code=code
                           )


@app.route('/admin', methods=('GET', 'POST'))
@admin_required
def admin():
    users = []
    if (request.method == 'POST'):
        forms = request.form.to_dict()
        for email, permission in forms.items():
            try:
                user = User.query.filter_by(
                    email=email.lower(),
                ).first()

                if (permission == 'is_admin'):
                    if(user.is_admin):
                        user.is_admin = False
                    else:
                        user.is_admin = True
                        user.is_contributor = True
                        user.is_approved = True
                elif (permission == 'is_contributor'):
                    if(user.is_contributor):
                        user.is_admin = False
                        user.is_contributor = False
                    else:
                        user.is_contributor = True
                        user.is_approved = True
                elif (permission == 'is_approved'):
                    if(user.is_approved):
                        user.is_admin = False
                        user.is_contributor = False
                        user.is_approved = False
                    else:
                        user.is_approved = True
                db.session.commit()
            except Exception as e:
                error = getattr(e, 'message', repr(e))
                db.session.rollback()
    try:
        admin_email_list = app.config['ADMIN_LIST']
        users = User.query.filter(User.email.notin_(admin_email_list)).all()
    except Exception as e:
        error = getattr(e, 'message', repr(e))
        flash(error, 'error')
    return render_template('user/admin.html', users=users)
