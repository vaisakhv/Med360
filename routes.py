from distutils.util import strtobool

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, LoginManager, login_user, current_user, logout_user
# from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash

from med360 import decodeSpecialties, get_age, Security, admin, covid_data
from models import User, Hospital, City, Role, app, db, Scheme
from views import (RegisterForm, SearchHospitalForm, FindBloodDonorForm, LoginForm,
                   ResetPasswordForm, ProfileUpdateForm,
                   ContactForm, SearchForm)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# mail = Mail()
# mail.init_app(app)

def is_auth():
    auth = False
    if current_user.is_authenticated:
        auth = True
    return auth


@login_manager.user_loader
def user_loader(uid):
    return User.query.get(int(uid))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("403.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")


@app.route("/about")
def about():
    return render_template("/about.html", auth=is_auth())


@app.route("/services")
def services():
    return render_template("/services.html", auth=is_auth())


@app.route('/contact')
def contact():
    form = ContactForm()
    if request.method == 'POST':
        return 'Form posted.'
    # elif request.method == 'GET':
    #     msg = Message(form.subject.data, sender='vais27@gmail.com', recipients=['vais27@gmail.com'])
    #     msg.body = """
    #           From: %s <%s>
    #           %s
    #           """ % (form.name.data, form.email.data, form.message.data)
    #     mail.send(msg)
    #     return render_template('contact.html', form=form, success=True)
    return render_template('contact.html', form=form, auth=is_auth())


@app.route('/')
def index():
    india_val = [[0]]
    global_val = {"Global": '0'}
    if current_user.is_authenticated:
        india_val, global_val = covid_data()
    print(india_val[0], '\n', global_val['Global'])
    return render_template('index.html', auth=is_auth(), current_user=current_user, india=india_val, world=global_val)


@app.route('/check/<username>')
def check(username):
    user = User.find_by_username(username=username)
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
        user = User.find_by_username(username=uname)
        print('found ', user.username)
        if uname != '' or passw != '':
            if user is not None:
                if check_password_hash(user.password, passw):
                    print(user.username)
                    login_user(user)
                    try:
                        user_role = Role.find_by_id(user.role)
                    except Exception as e:
                        print(str(e))
                    print('role_name=', user_role.name, 'role_id=', user_role.id)
                    if user_role.name == "admin":
                        print("Enabling admin view")
                        admin.add_view(ModelView(User, db.session))
                        admin.add_view(ModelView(Hospital, db.session))
                        admin.add_view(ModelView(City, db.session))
                        admin.add_view(ModelView(Role, db.session))
                    next = request.args.get('next')
                    return redirect(next or url_for('index'))
                flash('Invalid password for user ' + user.username)
                return render_template("login_2.html", form=form)
            flash('Invalid username ')
            return render_template("login_2.html", form=form)
        flash('Invalid username or/and password')
        return render_template("login_2.html", form=form)
    elif 'passw' in form.errors.keys():
        flash('Invalid password')
        return render_template("login_2.html", form=form)
    elif current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("login_2.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/me')
@login_required
def view_profile():
    user_role = Role.find_by_id(current_user.role)
    return render_template('profile_page.html', title='My Details', user=current_user, role=user_role.name,
                           auth=is_auth())


@app.route("/resetpwd", methods=["GET", "POST"])
def resetPassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        uname = form.uname.data
        dob = form.dob.data
        user = User.find_by_username(uname)
        if user is not None:
            print(user.name)
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
    return render_template("resetpwd.html", form=form, auth=is_auth())


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    form.city.choices = [(city.id, city.name) for city in City.find_by_state('Kerala')]
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        uname = form.uname.data
        mail = form.mail.data
        passw = form.passw.data
        conf_passw = form.conf_passw.data
        pan = form.pan.data
        name = form.name.data
        sex = form.sex.data
        dob = form.dob.data
        bld_grp = form.bld_grp.data
        addr = form.addr.data
        state = form.state.data
        city = City.get_by_id(form.city.data)
        po_num = form.pincode.data
        mobile = form.mobile.data
        aadhar = form.aadhar.data
        organ_donation = bool(strtobool(form.organ_donation.data))
        bld_donation = bool(strtobool(form.bld_donation.data))
        user_role = int(form.role.data)
        print('selected role id is ', user_role)
        r = Role.find_by_id(user_role)
        print('selected role name is ', r.name)
        existing_user = User.query.filter_by(mobile=mobile, email=mail, username=uname, aadhar=aadhar, pan=pan).first()
        if existing_user is None:
            if conf_passw == passw:
                new_user = User(username=uname, email=mail, password=generate_password_hash(passw, method='sha256'),
                                pan=pan, city=city.name, age=get_age(dob),
                                name=name, sex=sex, dob=dob,
                                bld_grp=bld_grp, addr=addr, state=state, po_num=po_num, mobile=mobile, aadhar=aadhar,
                                organ_donation=bool(organ_donation), bld_donaton=bool(bld_donation), role=user_role)
                new_user.save_to_db()
                return redirect(url_for("login"))
            print("Password don't match")
            flash(message="Passwords don't match!!")
            return render_template("register.html", form=form)
        print('user existing')
        flash(message='A user with same details already exists')
        return render_template("register.html", form=form)
    return render_template("register.html", form=form)


@app.route('/update', methods=['POST', 'GET'])
@login_required
def update_profile():
    user = User.find_by_username(username=current_user.username)
    city = City.get_id_by_name(_name=current_user.city)
    form = ProfileUpdateForm(city=city.id, bld_grp=user.bld_grp, sex=user.sex, organ_donation=bool(user.organ_donation),
                             bld_donation=bool(user.bld_donation))
    form.city.choices = [(city.id, city.name) for city in City.find_by_state('Kerala')]

    role = Role.find_by_id(current_user.role)
    print('user role is ', role.name)
    print(form.validate_on_submit())
    print(form.errors)
    print('log')
    if form.validate_on_submit():
        user.uname = form.uname.data
        user.mail = form.mail.data
        user.dob = form.dob.data
        user.age = get_age(form.dob.data)
        user.pan = form.pan.data
        user.name = form.name.data
        user.sex = form.sex.data
        user.bld_grp = form.bld_grp.data
        user.addr = form.addr.data
        user.state = form.state.data
        curr_city = City.get_by_id(form.city.data)
        user.city = curr_city.name
        user.po_num = form.pincode.data
        user.mobile = form.mobile.data
        user.aadhar = form.aadhar.data
        user_role = int(form.role.data)
        user.organ_donation = bool(strtobool(form.organ_donation.data))
        user.bld_donation = bool(strtobool(form.bld_donation.data))
        role = Role.find_by_id(user_role)
        user.role = role.id
        user.save_to_db()
        print('user_id=', user.id, 'selected_role_id=', role.id, 'selected_role_name=', role.name)
        print('user_id=', user.id, 'role_id_db=', user.role, )
        return redirect(url_for("view_profile"))
    return render_template("update_profile.html", form=form, role=role.name)


@app.route('/remove_acnt', methods=['POST', 'GET'])
@login_required
def remove_acnt():
    user = User.find_by_username(username=current_user.username)
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
    cities = City.find_by_state(state)
    city_array = []
    for city in cities:
        city_obj = {'id': city.id, 'name': city.name}
        city_array.append(city_obj)
    return jsonify({'cities': city_array})


@app.route("/search_hospital", methods=["GET", "POST"])
@login_required
def search_hospital():
    form = SearchHospitalForm()
    form.city.choices = [(city.id, city.name) for city in City.find_by_state('Kerala')]
    if form.is_submitted():
        city = City.get_by_id(form.city.data)
        state_name = city.name
        spec = form.spec.data
        scheme_id = form.scheme.data
        if spec != "None" and state_name is not '' and not state_name.isspace():
            hosps = Hospital.find_by_spec_and_state(_spec=spec, _state=state_name).all()
            if scheme_id != 0:
                filtered = []
                scheme = Scheme.find_by_scheme_id(scheme_id)
                print(scheme.name)
                print(scheme.partner_hospitals)
                for a_hosp in hosps:
                    if a_hosp in scheme.partner_hospitals.all():
                        filtered.append(a_hosp)
                print(filtered)
                if len(filtered) <= 0:
                    flash("No Hospitals found, why don't you try without the Scheme filter!!")
                    return render_template("search_hospital.html", current_user=current_user, form=form)
                return render_template('searchResult.html', data=filtered, current_user=current_user, auth=is_auth(),
                                       searchterm=state_name, encrypt=Security.encrypt)
            print("results form spec for ", decodeSpecialties(spec)[0])
            if len(hosps.all()) > 0:
                return render_template('searchResult.html', data=hosps, current_user=current_user, auth=is_auth(),
                                       searchterm=state_name, encrypt=Security.encrypt)
            else:
                print('no hospitals with ', spec)
                flash("No Hospitals found, why don't you try without the Speciality filter!!")
                return render_template("search_hospital.html", current_user=current_user, form=form)
        elif state_name is not '' and not state_name.isspace():
            hosp = Hospital.find_by_state(state_name)
            if len(hosp.all()) > 0:
                if scheme_id != 0:
                    scheme = Scheme.find_by_scheme_id(scheme_id)
                    filtered = []
                    for a_hosp in hosp:
                        if a_hosp in scheme.partner_hospitals.all():
                            filtered.append(a_hosp)
                    print(filtered)
                    if len(filtered) <= 0:
                        flash("No Hospitals found, why don't you try without the Scheme filter!!")
                        return render_template("search_hospital.html", current_user=current_user, form=form)
                    return render_template('searchResult.html', data=filtered, current_user=current_user,
                                           auth=is_auth(),
                                           searchterm=state_name, encrypt=Security.encrypt)
                return render_template('searchResult.html', data=hosp, current_user=current_user, searchterm=state_name,
                                       encrypt=Security.encrypt, auth=is_auth())
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
    selected_id = Security.decrypt(str(request.args.get('hosp_id')))
    hosp = Hospital.find_by_id(int(selected_id))
    specs_up = hosp.hosp_spec_upgraded
    specs_emp = hosp.hosp_spec_empanl
    dec_specs_up = decodeSpecialties(specs_up)
    dec_specs_emp = decodeSpecialties(specs_emp)
    return render_template('hospitalDetails.html', title='Hospital Details', data=hosp, specs_up=dec_specs_up,
                           specs_emp=dec_specs_emp, auth=is_auth())


@app.route('/search_blood_donor', methods=['POST', 'GET'])
@login_required
def search_blood_donor():
    form = FindBloodDonorForm()
    form.city.choices = [(city.id, city.name) for city in City.find_by_state('Kerala')]
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


@app.route('/hosp_by_scheme')
def search_hosp_by_scheme():
    pass


@app.route('/scheme_by_hosp')
def search_scheme_by_hosp():
    hosp_id = 17
    hosp = Hospital.find_by_id(hosp_id)
    scheme_list = hosp.Schemes


def find_hosp_by_scheme():
    id = 8
    scheme = Scheme.find_by_scheme_id(id)
    parter_hosps = scheme.partner_hospitals


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.is_submitted():
        search_term = form.search.data
        results = Hospital.find_by_name(_name=search_term)
        print(results)
        return render_template('keyword_search.html', form=form, results=results, encrypt=Security.encrypt,
                               query=search_term)
    return render_template('keyword_search.html', form=form)


def __init__(self, **kwargs):
    for key, value in kwargs.items():
        setattr(self, key, value)


if __name__ == '__main__':
    app.run()
