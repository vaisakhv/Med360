from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, LoginManager, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import SelectField

from med360 import app, decodeSpecialties, spec_code_dict, Security
from models import User, Hospital, City, get_all_states


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


@app.route('/')
def index():
    auth = False
    if current_user.is_authenticated:
        auth = True
    return render_template('index.html', auth=auth, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        user = User.find_user_by_username(username=uname)
        if user is not None:
            if check_password_hash(user.password, passw):
                print(user.name)
                print(user.password)
                login_user(user)
                next = request.args.get('next')
                return redirect(next or url_for('index'))
            else:
                flash(message='Invalid password for user ' + user.username)
        else:
            flash(message='Invalid username and password')
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/me')
@login_required
def view_profile():
    return render_template('profile_page.html', title='My Details', user=current_user)


@app.route("/resetpwd", methods=["GET", "POST"])
def resetPassword():
    if request.method == "POST":
        uname = request.form["uname"]
        dob = datetime.date(datetime.strptime(request.form["dob"], "%Y-%m-%d"))
        user = User.find_user_by_username(uname)
        if user is not None:
            passw = request.form["passw"]
            conf_passw = request.form["conf_passw"]
            if conf_passw == passw:
                if user.dob == dob:
                    if not check_password_hash(user.password, passw):
                        user.reset_password(username=uname,
                                            new_password=generate_password_hash(password=passw, method='sha256'))
                        user.save_to_db()
                        return redirect(url_for("login"))
                    else:
                        flash(message='You cannot use the previous password as the new password')
                else:
                    print(user.dob, dob)
                    flash(message='Date of Birth does not match with the user details!!')
            else:
                flash(message='Passwords doesnt match!!')
        else:
            flash(message='Username not found')
    return render_template("resetpwd.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        # age = request.form['age']
        pan = request.form['pan']
        name = request.form['name']
        sex = request.form['sex']
        dob = request.form['dob']
        bld_grp = request.form['bld_grp']
        addr = request.form['addr']
        state = request.form['state']
        po_num = request.form['pincode']
        mobile = request.form['mobile']
        aadhar = request.form['aadhar']
        organ_donation = request.form['organ_donation']
        bld_donation = request.form['bld_donation']
        existing_user = User.query.filter_by(mobile=mobile, email=mail, username=uname, aadhar=aadhar, pan=pan).first()
        if existing_user is None:
            new_user = User(username=uname, email=mail, password=generate_password_hash(passw, method='sha256'),
                            pan=pan,
                            name=name, sex=sex, dob=datetime.date(datetime.strptime(dob, "%Y-%m-%d")),
                            bld_grp=bld_grp, addr=addr, state=state, po_num=po_num, mobile=mobile, aadhar=aadhar,
                            organ_donation=bool(organ_donation), bld_donaton=bool(bld_donation))
            new_user.save_to_db()
            return redirect(url_for("login"))
        else:
            print('user existing')
            flash(message='A user with same details already exists')
    return render_template("register.html")


@app.route('/remove_acnt', methods=['POST', 'GET'])
@login_required
def remove_acnt():
    user = User.find_user_by_username(username=current_user.username)

    try:
        user.remove_from_db()
        return redirect(url_for("login"))
    except Exception as e:
        print(str(e))


@app.route("/newHospital", methods=["GET", "POST"])
def add_hospital():
    if request.method == "POST":
        hosp_name = request.form['hosp_name']
        hosp_type = request.form['hosp_type']
        hosp_addr = request.form['hosp_addr']
        hosp_email = request.form['hosp_email']
        hosp_num = request.form['hosp_num']
        hosp_spec_empnl = request.form['hosp_spec_empnl']
        hosp_spec_up = request.form['hosp_spec_up']
        hosp = Hospital(hosp_name=hosp_name, hosp_type=hosp_type, hosp_addr=hosp_addr, hosp_contact_mail=hosp_email,
                        hosp_contact_no=hosp_num, hosp_spec_empanl=hosp_spec_empnl, hosp_spec_upgraded=hosp_spec_up)
        hosp.save_to_db()
        return redirect(url_for("login"))  # login for hosp
    return render_template("register.html")  # return to hosp registration


@app.route('/city/<state>')
@login_required
def getDist(state):
    cities = City.find_city_by_state(state)
    city_array = []
    for city in cities:
        city_obj = {'id': city.id, 'name': city.name}
        city_array.append(city_obj)
    return jsonify({'cities': city_array})


class Form(FlaskForm):
    states_in_db = get_all_states()
    spec_codes = spec_code_dict()
    state = SelectField('state', choices=states_in_db)
    city = SelectField('city', choices=[])
    spec = SelectField('spec', choices=spec_codes)


@app.route("/search_hospital", methods=["GET", "POST"])
@login_required
def search_hospital():
    form = Form()
    form.city.choices = [(city.id, city.name) for city in City.find_city_by_state('Kerala')]
    if request.method == 'POST':
        state_id = request.form['city']
        city = City.get_by_id(state_id)
        state_name = city.name
        spec = request.form['spec']
        if spec != "None" and state_name is not '' and not state_name.isspace():
            hosps = Hospital.find_hosp_by_spec_and_state(_spec=spec, _state=state_name)
            print("results form spec for ", decodeSpecialties(spec)[0])
            if len(hosps.all()) > 0:
                return render_template('searchResult.html', data=hosps, current_user=current_user,
                                       searchterm=state_name)
            else:
                print('no hospitals with ', spec)
                flash(message="No Hospitals found, why don't you try without the Speciality filter!!")
        elif state_name is not '' and not state_name.isspace():
            hosp = Hospital.find_hosp_by_state(state_name)
        else:
            flash(message="Enter a valid query")
    return render_template("search_hospital.html", current_user=current_user, form=form)


@app.route("/hospitalDetails", methods=["GET", "POST"])
@login_required
def hospital_details():
    selected_id = request.args.get('hosp_id')
    hosp = Hospital.find_hosp_by_id(int(selected_id))
    specs_up = hosp.hosp_spec_upgraded
    specs_emp = hosp.hosp_spec_empanl
    dec_specs_up = decodeSpecialties(specs_up)
    dec_specs_emp = decodeSpecialties(specs_emp)
    return render_template('hospitalDetails.html', title='Hospital Details', data=hosp, specs_up=dec_specs_up,
                           specs_emp=dec_specs_emp)


if __name__ == '__main__':
    app.run()
