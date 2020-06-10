from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)


# import admin_view for displaying model. a
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_city_by_state(cls, _state):
        return cls.query.filter_by(state=_state).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __init__(self, _id, _name, _state):
        self.id = _id
        self.name = _name
        self.state = _state


class Hospital(db.Model):
    hosp_id = db.Column(db.Integer, primary_key=True)
    hosp_name = db.Column(db.String(100), unique=True, nullable=False)
    hosp_addr = db.Column(db.String(200), nullable=False)
    hosp_spec_empanl = db.Column(db.String(200))
    hosp_spec_upgraded = db.Column(db.String(200))
    hosp_contact_no = db.Column(db.Integer())
    hosp_contact_mail = db.Column(db.String(80))
    hosp_type = db.Column(db.String(30), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_hosp_by_name(cls, _name):
        return cls.query.filter_by(hosp_name=_name)

    @classmethod
    def find_hosp_by_id(cls, _id):
        return cls.query.filter_by(hosp_id=_id).first()

    @classmethod
    def find_hosp_by_state(cls, _state):
        return cls.query.filter(cls.hosp_addr.contains(_state))

    @classmethod
    def find_hosp_by_spec_and_state(cls, _spec, _state):
        return cls.query.filter(cls.hosp_addr.contains(_state), cls.hosp_spec_upgraded.contains(_spec))

    def __init__(self, hosp_name, hosp_addr, hosp_spec_empanl, hosp_spec_upgraded, hosp_contact_no,
                 hosp_contact_mail, hosp_type):
        # self.hosp_id = hosp_id
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
    age = db.Column(db.Integer(), nullable=False)
    pan = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    bld_grp = db.Column(db.String(5), nullable=False)
    addr = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    po_num = db.Column(db.Integer(), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False, unique=True)
    aadhar = db.Column(db.Integer(), nullable=False, unique=True)
    organ_donation = db.Column(db.Boolean(), nullable=True)
    bld_donation = db.Column(db.Boolean(), nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_blood_donor(cls, blood_type, location):
        users = cls.query.filter(cls.bld_donation == True, cls.bld_grp == blood_type,
                                 cls.addr.contains(location) | cls.state.contains(location) | cls.city.contains(
                                     location)).all()
        return users

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def reset_password(cls, username, new_password):
        user = User.find_user_by_username(username=username)
        user.password = new_password
        user.save_to_db()

    def __init__(self, username, email, password, pan, name, sex, dob, bld_grp, addr, state, po_num, mobile, aadhar,
                 organ_donation, bld_donaton, city, age):
        self.username = username
        self.email = email
        self.password = password
        self.age = age
        self.pan = pan
        self.name = name
        self.sex = sex
        self.dob = dob
        self.bld_grp = bld_grp
        self.addr = addr
        self.state = state
        self.city = city
        self.po_num = po_num
        self.mobile = mobile
        self.aadhar = aadhar
        self.organ_donation = organ_donation
        self.bld_donation = bld_donaton


if __name__ == "__main__":
    db.create_all()
