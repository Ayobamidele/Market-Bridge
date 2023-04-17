from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import phonenumbers
from .models import User
from flask_login import current_user
from phonenumbers import geocoder


# from flask_login import login_required, current_user

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                        validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign-up", render_kw={"class": "btn btn-outline-purple btn-dark"})

    def validate_phone(self, phone):
        try:
            phone_number = phonenumbers.parse(phone.data, None)
            country_prefix = geocoder.region_code_for_number(phone_number)
            p = phonenumbers.parse(str(phone_number.national_number), str(country_prefix))
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UserEdit(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])

    save = SubmitField("Save")

    cancel = SubmitField(label='Cancel',
                         render_kw={'form-novalidate': True, 'class': ' btn-warning'})

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # check if user is owner of email
        # Check if other user has the email
        if current_user.email != email.data:
            if user is not None:
                raise ValidationError('Please use a different email address.')


class PhoneChangeForm(FlaskForm):
    phone = StringField('Phone', validators=[])
    submit = SubmitField('Submit')
    cancel = SubmitField(label='Cancel',
                         render_kw={'form-novalidate': True, 'class': ' btn-warning'})

    def validate_phone(self, phone):
        try:
            phone_number = phonenumbers.parse(phone.data, None)
            country_prefix = geocoder.region_code_for_number(phone_number)
            p = phonenumbers.parse(str(phone_number.national_number), str(country_prefix))
            if not phonenumbers.is_valid_number(p):
                raise ValidationError("Invalid phone number")
        except:
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign In")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField('Submit')
