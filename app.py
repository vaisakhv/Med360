from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, LoginManager, login_user, UserMixin, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12345'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)


class Hospital(db.Model):
    hosp_id = db.Column(db.Integer, primary_key=True)
    hosp_name = db.Column(db.String(100), unique=True, nullable=False)
    hosp_addr = db.Column(db.String(200), nullable=False)
    hosp_spec_empanl = db. Column(db.String(200))
    hosp_spec_upgraded = db. Column(db.String(200))
    hosp_contact_no = db.Column(db.Integer())
    hosp_contact_mail = db.Column(db.String(80))
    hosp_type = db.Column(db.String(30), nullable=False)

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_hosp_by_name(cls, _name):
        return cls.query.filter_by(hosp_name=_name)

    # Class method which finds user from DB by id
    @classmethod
    def find_hosp_by_id(cls, _id):
        return cls.query.filter_by(hosp_id=_id).first()

    @classmethod
    def find_hosp_by_state(cls, _state):
        return cls.query.filter(cls.hosp_addr.contains(_state))

    def __init__(self, hosp_id, hosp_name, hosp_addr, hosp_spec_empanl, hosp_spec_upgraded, hosp_contact_no,
                 hosp_contact_mail, hosp_type):
        self.hosp_id = hosp_id
        self.hosp_name = hosp_name
        self.hosp_addr = hosp_addr
        self.hosp_spec_empanl = hosp_spec_empanl
        self.hosp_spec_upgraded = hosp_spec_upgraded
        self.hosp_contact_no = hosp_contact_no
        self.hosp_contact_mail = hosp_contact_mail
        self.hosp_type = hosp_type


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    # age = db.Column(db.Integer(), nullable=False)
    pan = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    bld_grp = db.Column(db.String(5), nullable=False)
    addr = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    po_num = db.Column(db.Integer(), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False, unique=True)
    aadhar = db.Column(db.Integer(), nullable=False, unique=True)
    organ_donation = db.Column(db.Boolean(), nullable=True)
    bld_donation = db.Column(db.Boolean(), nullable=True)

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def reset_password(cls, username, new_password):
        user = User.find_user_by_username(username=username)
        user.password = new_password
        user.save_to_db()

    def __init__(self, username, email, password, pan, name, sex, dob, bld_grp, addr, state, po_num, mobile, aadhar,
                 organ_donation, bld_donaton):
        self.username = username
        self.email = email
        self.password = password
        # self.age = age
        self.pan = pan
        self.name = name
        self.sex = sex
        self.dob = dob
        self.bld_grp = bld_grp
        self.addr = addr
        self.state = state
        self.po_num = po_num
        self.mobile = mobile
        self.aadhar = aadhar
        self.organ_donation = organ_donation
        self.bld_donation = bld_donaton


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
                # session['username'] = uname
                print(user.name)
                print(user.password)
                login_user(user)
                next = request.args.get('next')
                return redirect(next or url_for('index'))
            else:
                flash(message='Invalid password for user '+user.username)
        else:
            flash(message='Invalid username and password')
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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
                        user.reset_password(username=uname, new_password=generate_password_hash(password=passw, method='sha256'))
                        user.save_to_db()
                        return redirect(url_for("login"))
                    else:
                        flash(message='You cannot use the previous password as the new password')
                else:
                    print(user.dob, dob)
                    flash(message='Date of Birth does not match with the user details')
            else:
                flash(message='Passwords doesnt match')
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
            new_user = User(username=uname, email=mail, password=generate_password_hash(passw, method='sha256'), pan=pan,
                            name=name, sex=sex, dob=datetime.date(datetime.strptime(dob, "%Y-%m-%d")),
                            bld_grp=bld_grp, addr=addr, state=state, po_num=po_num, mobile=mobile, aadhar=aadhar,
                            organ_donation=bool(organ_donation), bld_donaton=bool(bld_donation))
            print(new_user.name)
            print(new_user.password)
            new_user.save_to_db()
            return redirect(url_for("login"))
        else:
            print('user existing')
            flash(message='A user with same details already exists')
    return render_template("register.html")


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
        db.session.add(hosp)
        db.session.commit()
        return redirect(url_for("login"))#login for hosp
    return render_template("register.html")#return to hosp registration


@app.route("/search_hospital",  methods=["GET", "POST"])
@login_required
def search_hospital():
    if request.method == 'POST':
        statename = request.form['searchTerm']
        print(statename)
        if statename is not '' and not statename.isspace():
            hosp = Hospital.find_hosp_by_state(statename)
            if len(hosp.all()) > 0:
                return render_template('searchResult.html', data=hosp, current_user=current_user, searchterm=statename)
            else:
                flash(message='No Hospitals found')
        else:
            flash(message="Enter a valid query")
    return render_template("search_hospital.html", current_user=current_user)


@app.route("/hospitalDetails", methods=["GET", "POST"])
@login_required
def hospital_details():
    selected_id = request.args.get('hosp_id')
    hosp = Hospital.find_hosp_by_id(int(selected_id))
    return render_template('hospitalDetails.html', title='Hospital Details', data=hosp)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
