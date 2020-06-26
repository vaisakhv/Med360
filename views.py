from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, PasswordField, validators, TextAreaField, \
    SubmitField
from wtforms.fields.html5 import DateField

from med360 import get_all_states, get_all_states_for_donors, spec_code_dict, get_all_roles


class SearchHospitalForm(FlaskForm):
    states_in_db = get_all_states()
    spec_codes = spec_code_dict()
    state = SelectField('state', choices=states_in_db)
    city = SelectField('city', choices=[], coerce=int)
    spec = SelectField('spec', choices=spec_codes)


class FindBloodDonorForm(FlaskForm):
    states_in_db = get_all_states_for_donors()
    state = SelectField('state', choices=states_in_db)
    city = SelectField('city', choices=[])
    bld_grp = SelectField('bld_grp', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                              ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])


class LoginForm(FlaskForm):
    uname = StringField('uname', [validators.DataRequired("Please enter your username"), validators.Length(min=7)],
                        render_kw={'placeholder': 'Username'})
    passw = PasswordField('passw', [validators.DataRequired("Please enter you password"), validators.Length(min=7)],
                          render_kw={'placeholder': '*************'})


class ResetPasswordForm(FlaskForm):
    uname = StringField('uname', [validators.DataRequired('Please enter your username'), validators.Length(min=7)],
                        render_kw={'placeholder': 'Username'})
    passw = PasswordField('passw', [validators.DataRequired('Please enter a new password'), validators.Length(min=7)],
                          render_kw={'placeholder': 'Password'})
    conf_passw = PasswordField('conf_passw',
                               [validators.DataRequired('Please re-enter the new password'), validators.Length(min=7)],
                               render_kw={'placeholder': 'Confirm Password'})
    dob = DateField('dob', [validators.DataRequired('select a valid date')], format='%Y-%m-%d')


class RegisterForm(FlaskForm):
    states_in_db = get_all_states()
    roles_from_db = get_all_roles()
    role = SelectField('role', [validators.DataRequired('Please enter a valid Role')], choices=roles_from_db,
                       coerce=int)
    uname = StringField('uname', [validators.DataRequired('Please enter a valid Username'), validators.Length(min=7)],
                        render_kw={'placeholder': 'Username'})
    name = StringField('name', [validators.DataRequired('Please enter you name')],
                       render_kw={'placeholder': 'Name'})
    mail = StringField('mail', [validators.DataRequired('Please enter a valid email'),
                                validators.Email('Please enter your valid email')], render_kw={'placeholder': 'Email'})
    mobile = IntegerField('mobile', [validators.DataRequired('Please enter you mobile number')],
                          render_kw={'placeholder': 'Mobile Number'})
    addr = StringField('addr', [validators.DataRequired('Please enter you Address')],
                       render_kw={'placeholder': 'Address'})
    state = SelectField('state', [validators.DataRequired('Please select you state')], choices=states_in_db)
    city = SelectField('city', [validators.DataRequired('Please select your current residing city')], choices=[],
                       coerce=int)
    pincode = IntegerField('pincode', [validators.DataRequired('Please enter you pincode')],
                           render_kw={'placeholder': 'Pincode'})
    passw = PasswordField('passw', [validators.DataRequired('Please enter a valid password'), validators.Length(min=7)],
                          render_kw={'placeholder': 'Password'})
    conf_passw = PasswordField('conf_passw',
                               [validators.DataRequired('Please re-enter the password'), validators.Length(min=7)],
                               render_kw={'placeholder': 'Confirm Password'})
    # age = IntegerField('age', [validators.DataRequired('Please enter a valid age')], render_kw={'placeholder': 'Age'})
    dob = DateField('dob', [validators.DataRequired('select a valid date')], format='%Y-%m-%d')
    pan = StringField('pan', [validators.DataRequired('Enter your PAN number'), validators.Length(max=10, min=10)],
                      render_kw={'placeholder': 'PAN'})
    aadhar = StringField('aadhar',
                         [validators.DataRequired('Please enter you Aadhar number'), validators.Length(max=14)],
                         render_kw={'placeholder': 'Aadhaar'})
    sex = SelectField('sex', validators=[validators.DataRequired("Please select one")],
                      choices=[('Male', 'Male'), ('Female', 'Female')])
    bld_grp = SelectField('bld_grp', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                              ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    organ_donation = SelectField('organ_donation', [validators.DataRequired('Please select one')],
                                 choices=[('True', 'Yes'), ('False', 'No')])
    bld_donation = SelectField('bld_donation', [validators.DataRequired('Please select one')],
                               choices=[('True', 'Yes'), ('False', 'No')])


class ProfileUpdateForm(FlaskForm):
    states_in_db = get_all_states()
    roles_from_db = get_all_roles()
    role = SelectField('role', [validators.DataRequired('Please enter a valid Role')], choices=roles_from_db,
                       coerce=int)
    uname = StringField('uname', render_kw={'disabled': 'disabled'})
    name = StringField('name')
    mail = StringField('mail', [validators.DataRequired('Please enter a valid email'),
                                validators.Email('Please enter your valid email')])
    mobile = IntegerField('mobile', [validators.DataRequired('Please enter you mobile number')],
                          render_kw={'placeholder': 'Mobile Number'})
    addr = StringField('addr', [validators.DataRequired('Please enter you Address')],
                       render_kw={'placeholder': 'Address'})
    state = SelectField('state', [validators.DataRequired('Please select you state')], choices=states_in_db)
    city = SelectField('city', [validators.DataRequired('Please select your current residing city')], choices=[],
                       coerce=int)
    pincode = IntegerField('pincode', [validators.DataRequired('Please enter you pincode')],
                           render_kw={'placeholder': 'Pincode'})
    # age = IntegerField('age', [validators.DataRequired('Please enter a valid age')], render_kw={'placeholder': 'Age'})
    dob = DateField('dob', [validators.DataRequired('select a valid date')], format='%Y-%m-%d')
    pan = StringField('pan', [validators.DataRequired('Enter your PAN number'), validators.Length(max=10, min=10)],
                      render_kw={'placeholder': 'PAN'})
    aadhar = StringField('aadhar',
                         [validators.DataRequired('Please enter you Aadhar number'), validators.Length(max=14)],
                         render_kw={'placeholder': 'Aadhaar'})
    sex = SelectField('sex', validators=[validators.DataRequired("Please select one")],
                      choices=[('Male', 'Male'), ('Female', 'Female')])
    bld_grp = SelectField('bld_grp', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                              ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    organ_donation = SelectField('organ_donation', [validators.DataRequired('Please select one')],
                                 choices=[('True', 'Yes'), ('False', 'No')])
    bld_donation = SelectField('bld_donation', [validators.DataRequired('Please select one')],
                               choices=[('True', 'Yes'), ('False', 'No')])


class ContactForm(FlaskForm):
    name = StringField("Name", [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired()])
    subject = StringField("Subject", [validators.DataRequired()])
    message = TextAreaField("Message", [validators.DataRequired()])
    submit = SubmitField("Send")
