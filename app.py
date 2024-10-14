from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    if 'username' in session:
        return redirect(f'/users/{session["username"]}')
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        return redirect('/secret')
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors.append('Invalid users/password')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret():
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    return render_template('secret.html')

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash('Goodbye!', 'info')
    return redirect('/')

@app.route('/users/<string:username>')
def show_user(username):
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    feedback = user.feedback
    return render_template('user.html', user=user, feedbacks=feedback)

@app.route('/users/<string:username>/delete', methods=["POST"])
def delete_user(username):
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    if username == session['username']:
        user = User.query.filter_by(username=username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        return redirect('/')
    return redirect(f'/users/{session["username"]}')

@app.route('/users/<string:username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    if username == session['username']:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        return render_template('feedback.html', form=form)
    return redirect(f'/users/{session["username"]}')

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    if feedback.username == session['username']:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        return render_template('feedback.html', form=form)
    return redirect(f'/users/{session["username"]}')

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session:
        flash('Please login first')
        return redirect('/login')
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    return redirect(f'/users/{session["username"]}')