from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, PasswordField, RadioField, validators
from wtforms.fields.html5 import DateField

from med360 import get_all_states, get_all_states_for_donors, spec_code_dict


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
                          render_kw={'placeholder': 'Password'})


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
    uname = StringField('uname', [validators.DataRequired('Please enter a valid Username'), validators.Length(min=7)])
    name = StringField('name', [validators.DataRequired('Please enter you name')])
    mail = StringField('mail', [validators.DataRequired('Please enter a valid email'), validators.Email('Please enter '
                                                                                                        'your valid '
                                                                                                        'email')])
    mobile = IntegerField('mobile', [validators.DataRequired('Please enter you mobile number')])
    addr = StringField('addr', [validators.DataRequired('Please enter you Address')])
    state = SelectField('state', [validators.DataRequired('Please select you state')], choices=states_in_db)
    city = SelectField('city', [validators.DataRequired('Please select your current residing city')], choices=[],
                       coerce=int)
    pincode = IntegerField('pincode', [validators.DataRequired('Please enter you pincode')])
    passw = PasswordField('passw', [validators.DataRequired('Please enter a valid password'), validators.Length(min=7)])
    conf_passw = PasswordField('conf_passw',
                               [validators.DataRequired('Please re-enter the password'), validators.Length(min=7)])
    age = IntegerField('age', [validators.DataRequired('Please enter a valid age')])
    dob = DateField('dob', [validators.DataRequired('select a valid date')], format='%Y-%m-%d')
    pan = StringField('pan', [validators.DataRequired('Enter your PAN number'), validators.Length(max=10, min=10)])
    aadhar = StringField('aadhar',
                         [validators.DataRequired('Please enter you Aadhar number'), validators.Length(max=14)])
    sex = RadioField('sex', validators=[validators.DataRequired("Please select one")],
                     choices=[('Male', 'Male'), ('Female', 'Female')])
    bld_grp = SelectField('bld_grp', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                              ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    organ_donation = RadioField('organ_donation', [validators.DataRequired('Please select one')],
                                choices=[('True', 'Yes'), ('False', 'No')])
    bld_donation = RadioField('bld_donation', [validators.DataRequired('Please select one')],
                              choices=[('True', 'Yes'), ('False', 'No')])
