from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import TextArea

from .models import User


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'username', validators=[DataRequired(),
                                Length(min=3, max=25)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=4, max=20)]
    )
    confirm = PasswordField('Verify password',
         [DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AskForm(Form):
    title = StringField('title', validators=[DataRequired()])
    text = TextAreaField('text', validators=[DataRequired()])


class AnswerForm(Form):
    text = TextAreaField('text', validators=[DataRequired()])
