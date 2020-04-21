from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SelectField

from . import db


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
    def find_city_by_state(cls, state):
        return cls.query.filter_by(state=state).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __init__(self, id, name, state):
        self.id = id
        self.name = name
        self.state = state


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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

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


class Form(FlaskForm):
    states_in_db = [(r[0], r[0]) for r in db.session.query(City.state).distinct()]
    state = SelectField('state', choices=states_in_db)
    city = SelectField('city', choices=[])
