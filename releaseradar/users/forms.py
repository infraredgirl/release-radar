import flask_wtf
import wtforms
import flask_login

from releaseradar import messages, models


class RegistrationForm(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        'Username',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=20)
        ]
    )
    email = wtforms.StringField(
        'Email',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email()
        ]
    )
    password = wtforms.PasswordField(
        'Password',
        validators=[wtforms.validators.DataRequired()]
    )
    confirm_password = wtforms.PasswordField(
        'Confirm Password',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password')
        ]
    )
    submit = wtforms.SubmitField('Sign Up')

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user:
            raise wtforms.validators.ValidationError(messages.USERNAME_TAKEN)

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise wtforms.validators.ValidationError(messages.EMAIL_TAKEN)


class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.StringField(
        'Email',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email()
        ]
    )
    password = wtforms.PasswordField(
        'Password',
        validators=[wtforms.validators.DataRequired()]
    )
    remember = wtforms.BooleanField('Remember Me')
    submit = wtforms.SubmitField('Login')


class UpdateAccountForm(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        'Username',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=20)
        ]
    )
    email = wtforms.StringField(
        'Email',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email()
        ]
    )
    submit = wtforms.SubmitField('Update')

    def validate_username(self, username):
        if username.data != flask_login.current_user.username:
            user = models.User.query.filter_by(username=username.data).first()
            if user:
                raise wtforms.validators.ValidationError(
                    messages.USERNAME_TAKEN)

    def validate_email(self, email):
        if email.data != flask_login.current_user.email:
            user = models.User.query.filter_by(email=email.data).first()
            if user:
                raise wtforms.validators.ValidationError(messages.EMAIL_TAKEN)


class ArtistAddForm(flask_wtf.FlaskForm):
    artist_name = wtforms.StringField('Artist')
    submit = wtforms.SubmitField('Add Artist')


class RequestResetForm(flask_wtf.FlaskForm):
    email = wtforms.StringField(
        'Email',
        validators=[
            wtforms.validators.DataRequired(), wtforms.validators.Email()
        ]
    )
    submit = wtforms.SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is None:
            raise wtforms.validators.ValidationError(messages.EMAIL_NOT_FOUND)


class ResetPasswordForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField(
        'Password', validators=[wtforms.validators.DataRequired()])
    confirm_password = wtforms.PasswordField(
        'Confirm Password',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo('password')
        ]
    )
    submit = wtforms.SubmitField('Reset Password')
