from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, LoginManager, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from med360 import decodeSpecialties
from models import User, Hospital, City, app
from views import RegisterForm, SearchHospitalForm, FindBloodDonorForm, LoginForm, ResetPasswordForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# login_manager.needs_refresh_message = u"To protect your account, please reauthenticate to access this page."
# login_manager.refresh_view = "login"


@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


@app.route('/')
def index():
    auth = False
    if current_user.is_authenticated:
        auth = True
    return render_template('index.html', auth=auth, current_user=current_user)


@app.route('/check/<username>')
def check(username):
    user = User.find_user_by_username(username=username)
    print(user)
    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.uname.data
        passw = form.passw.data
        print(uname, passw)
        user = User.find_user_by_username(username=uname)
        print(user)
        if uname != '' or passw != '':
            user = User.find_user_by_username(username=uname)
            if user is not None:
                if check_password_hash(user.password, passw):
                    print(user.name)
                    print(user.password)
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('index'))
                flash('Invalid password for user ' + user.username)
                return render_template("login.html", form=form)
            flash('Invalid username and password')
            return render_template("login.html", form=form)
        flash('Invalid username and password')
        return render_template("login.html", form=form)
    elif 'passw' in form.errors.keys():
        flash('Invalid password')
        return render_template("login.html", form=form)
    elif current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


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
    form = ResetPasswordForm()
    if form.validate_on_submit():
        uname = form.uname.data
        dob = form.dob.data
        user = User.find_user_by_username(uname)
        print(user.name)
        if user is not None:
            passw = form.passw.data
            conf_passw = form.conf_passw.data
            if conf_passw == passw:
                if user.dob == dob:
                    if not check_password_hash(user.password, passw):
                        user.reset_password(username=uname,
                                            new_password=generate_password_hash(password=passw, method='sha256'))
                        user.save_to_db()
                        return redirect(url_for("login"))
                    flash(message='You cannot use the previous password as the new password')
                    return render_template("resetpwd.html", form=form)
                print(user.dob, dob)
                flash(message='Date of Birth does not match with the user details!!')
                return render_template("resetpwd.html", form=form)
            flash(message='Passwords doesnt match!!')
            return render_template("resetpwd.html", form=form)
        flash(message='Username not found')
        return render_template("resetpwd.html", form=form)
    return render_template("resetpwd.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    form.city.choices = [(city.id, city.name) for city in City.find_city_by_state('Kerala')]
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print(form.validate_on_submit())
    print(form.errors)
    print(form.city.data)
    if form.validate_on_submit():
        uname = form.uname.data
        mail = form.mail.data
        passw = form.passw.data
        conf_passw = form.conf_passw.data
        age = form.age.data
        pan = form.pan.data
        name = form.name.data
        sex = form.sex.data
        dob = form.dob.data
        print(dob)
        bld_grp = form.bld_grp.data
        addr = form.addr.data
        state = form.state.data
        city = City.get_by_id(form.city.data)
        po_num = form.pincode.data
        mobile = form.mobile.data
        aadhar = form.aadhar.data
        organ_donation = form.organ_donation.data
        bld_donation = form.bld_donation.data
        existing_user = User.query.filter_by(mobile=mobile, email=mail, username=uname, aadhar=aadhar, pan=pan).first()
        if existing_user is None:
            if conf_passw == passw:
                new_user = User(username=uname, email=mail, password=generate_password_hash(passw, method='sha256'),
                                pan=pan, city=city.name, age=age,
                                name=name, sex=sex, dob=dob,
                                bld_grp=bld_grp, addr=addr, state=state, po_num=po_num, mobile=mobile, aadhar=aadhar,
                                organ_donation=bool(organ_donation), bld_donaton=bool(bld_donation))
                new_user.save_to_db()
                return redirect(url_for("login"))
            print("Password don't match")
            flash(message="Passwords don't match!!")
            return render_template("register.html", form=form)
        print('user existing')
        flash(message='A user with same details already exists')
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)


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
def getDist(state):
    cities = City.find_city_by_state(state)
    city_array = []
    for city in cities:
        city_obj = {'id': city.id, 'name': city.name}
        city_array.append(city_obj)
    return jsonify({'cities': city_array})


@app.route("/search_hospital", methods=["GET", "POST"])
@login_required
def search_hospital():
    form = SearchHospitalForm()
    form.city.choices = [(city.id, city.name) for city in City.find_city_by_state('Kerala')]
    if form.is_submitted():
        city = City.get_by_id(form.city.data)
        state_name = city.name
        spec = form.spec.data
        if spec != "None" and state_name is not '' and not state_name.isspace():
            hosps = Hospital.find_hosp_by_spec_and_state(_spec=spec, _state=state_name)
            print("results form spec for ", decodeSpecialties(spec)[0])
            if len(hosps.all()) > 0:
                return render_template('searchResult.html', data=hosps, current_user=current_user,
                                       searchterm=state_name)
            else:
                print('no hospitals with ', spec)
                flash("No Hospitals found, why don't you try without the Speciality filter!!")
                return render_template("search_hospital.html", current_user=current_user, form=form)
        elif state_name is not '' and not state_name.isspace():
            hosp = Hospital.find_hosp_by_state(state_name)
            if len(hosp.all()) > 0:
                return render_template('searchResult.html', data=hosp, current_user=current_user, searchterm=state_name)
            else:
                flash('No Hospitals found!!')
                return render_template("search_hospital.html", current_user=current_user, form=form)
        else:
            flash("Enter a valid query")
            return render_template("search_hospital.html", current_user=current_user, form=form)
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


@app.route('/search_blood_donor', methods=['POST', 'GET'])
@login_required
def search_blood_donor():
    form = FindBloodDonorForm()
    form.city.choices = [(city.id, city.name) for city in City.find_city_by_state('Kerala')]
    if form.is_submitted():
        city = City.get_by_id(form.city.data)
        state_name = form.state.data
        bld_grp = form.bld_grp.data
        city_name = city.name
        print(state_name, bld_grp)
        donors = User.find_blood_donor(location=city_name, blood_type=bld_grp)
        len_of_donors = len(donors)
        if current_user in donors:
            print('found ', current_user.username, ' in donors list. removing it!')
            len_of_donors = len_of_donors - 1
        if len_of_donors > 0:
            return render_template('donor_search_result.html', data=donors, current_user=current_user, bld_grp=bld_grp)
        print('no donors with ', bld_grp)
        flash(message="No donors found!!")
        render_template("search_blood_donor.html", current_user=current_user, form=form)
    return render_template("search_blood_donor.html", current_user=current_user, form=form)


if __name__ == '__main__':
    app.run()
