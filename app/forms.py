from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
# from wtforms.widgets import TextArea

from .models import User


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
                    'username', validators=[DataRequired()]
                            )
    password = PasswordField(
                    'password', validators=[DataRequired()]
                            )


    def validate_login(self, field):
        if db.session.query(User).filter_by(login=field.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


class AskForm(Form):
    title = StringField('title', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])


class AnswerForm(Form):
    text = StringField('text', validators=[DataRequired()])
