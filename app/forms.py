from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

from .models import User


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = StringField(
                    'username', validators=[DataRequired()]
                            )
    password = PasswordField(
                    'password', validators=[DataRequired()]
                            )
    confirm = PasswordField(
                    'Repeat password',
                    validators=[
                                DataRequired(),
                                EqualTo('password',
                                        message='Password must match.')]
                            )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.error.append('Username already registered')
            return False
        return True
