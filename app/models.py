from app import db
from hashlib import md5


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(20))
    question = db.relationship('Question', backref='author', lazy='dynamic')
    answer = db.relationship('Answer', backref='author', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(self.username.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    text = db.Column(db.String(260))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.relationship('Answer', backref='answer', lazy='dynamic')

    def __repr__(self):
        return '<Question %r>' % (self.title)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qu_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    vote = db.Column(db.Integer, default=0)



    def upvote(self):
        self.vote = self.vote + 1
        return self.vote

    def get_id(self):
        return self.id

    @property
    def get_user(self):
        return User.query.get(int(self.user_id))

    def __repr__(self):
        return '<Answer %r>' % (self.text)
