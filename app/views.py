from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from datetime import datetime
from .forms import LoginForm, RegisterForm, AskForm, AnswerForm
from .models import User, Question, Answer
from markupsafe import Markup


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template("index.html",
                           title='Home',
                           user=user,
                           questions=questions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash('Registered seccesful! You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,
                                    password=form.password.data).first()
        if user is None:
            flash('Invalid username or password')
            return render_template('login.html', title='Sign In', form=form)
        flash('Login seccesful!')
        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # abort(404)
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    question = User.question.order_by(Question.timestamp.desc()).all()
    return render_template('user.html',
                           user=user,
                           question=question)


@app.route('/ask',  methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data,
                            text=form.text.data,
                            timestamp=datetime.utcnow(),
                            author=g.user)
        db.session.add(question)
        db.session.commit()
        flash('You question add!')
        return redirect(url_for('index'))
    return render_template('ask.html',
                           title='Create question',
                           form=form)


@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    question = Question.query.filter_by(id=id).first()
    if question is None:
        flash('Question not found.')
        return redirect(url_for('index'))
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(text=form.text.data,
                        timestamp=datetime.utcnow(),
                        author=g.user,
                        qu_id=id)
        try:
            db.session.add(answer)
            db.session.commit()
            flash('You answer post!')
        except Exception as e:
            db.session.rollback()
            flash(e, category='error')
        return redirect(url_for('question', id=id))
    return render_template('question.html',
                           question=question,
                           form=form)


@app.route('/voting', methods=['GET', 'POST'])
@login_required
def voting():
    id = request.args.get('id', None)
    q_id = request.args.get('q_id', None)
    if not id or not q_id:
        abort(404)
    answer = Answer.query.get_or_404(int(id))
    try:
        answer.upvote()
        db.session.add(answer)
        db.session.commit()
        flash('You are voted successfully. Thank you.', category='success')
    except Exception as e:
        db.session.rollback()
        flash(e, category='error')
    return redirect(url_for('question', id=q_id))
