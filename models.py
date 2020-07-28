from datetime import timedelta
from uuid import uuid4

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
    app.config.from_object(__name__)
    app.config['SECRET_KEY'] = 'kUwY%@tWnNXpigScMbSk7RYBZ#3BpVF3WG^u9oFje2Q$8h#e!^X4'
    Bootstrap(app)
    return app


app = create_app()
db = SQLAlchemy(app)
db.init_app(app)

#
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), unique=True)
    state = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def remove_from_db(self):
        db.session.remove(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_state(cls, _state):
        return cls.query.filter_by(state=_state).all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_id_by_name(cls, _name):
        return cls.query.filter_by(name=_name).first()

    def __init__(self, _id, _name, _state):
        self.id = _id
        self.name = _name
        self.state = _state


partners = db.Table('partners',
                    db.Column('uuid', db.String, db.ForeignKey('scheme.uuid')),
                    db.Column('hosp_id', db.String, db.ForeignKey('hospital.uuid'))
                    )


class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(50), nullable=False)
    creator = db.Column(db.String(52), nullable=False)
    approved_states = db.Column(db.String(52), nullable=False)
    approved_districts = db.Column(db.String(126), nullable=True)
    feature = db.Column(db.String(512), nullable=True)
    objective = db.Column(db.String(512), nullable=True)
    benefits = db.Column(db.String(512), nullable=True)
    eligibility = db.Column(db.String(256), nullable=True)
    partner_hospitals = db.relationship('Hospital', secondary=partners, backref=db.backref('Schemes'), lazy='dynamic')

    @classmethod
    def find_by_scheme_id(cls, id):
        return cls.query.filter_by(uuid=id).first()

    @classmethod
    def find_by_scheme_name(cls, name):
        return cls.query.filter(cls.name.like('%' + name + '%'))

    @classmethod
    def find_by_keyword(cls, keyword):
        columns = [column.key for column in Scheme.__table__.columns]
        results = []
        for col in columns:
            out = cls.query.filter(getattr(cls, col).like('%' + keyword + '%')).all()
            if len(out) > 0:
                results.append(out)
        return results

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return 'rm successful'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return 'commit successful'

    def __init__(self, name, feature, objective, benefits, eligibility, creator, approved_states,
                 approved_districts, ):
        self.uuid = str(uuid4())
        self.name = name
        self.feature = feature
        self.objective = objective
        self.benefits = benefits
        self.eligibility = eligibility
        self.creator = creator
        self.approved_states = approved_states
        self.approved_districts = approved_districts


class Hospital(db.Model):
    uuid = db.Column(db.String(40), unique=True)
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
        return 'commit successful'

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, _name):
        return cls.query.filter(cls.hosp_name.like('%' + _name + '%'))

    @classmethod
    def find_by_addr(cls, _addr):
        return cls.query.filter(cls.hosp_addr.ilike('%' + _addr + '%'))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(uuid=_id).first()

    @classmethod
    def find_by_state(cls, _state):
        return cls.query.filter(cls.hosp_addr.contains(_state))

    @classmethod
    def find_by_spec_and_state(cls, _spec, _state):
        return cls.query.filter(cls.hosp_addr.contains(_state), cls.hosp_spec_upgraded.contains(_spec))

    def __init__(self, hosp_name, hosp_addr, hosp_spec_empanl, hosp_spec_upgraded, hosp_contact_no,
                 hosp_contact_mail, hosp_type):
        self.uuid = str(uuid4())
        self.hosp_name = hosp_name
        self.hosp_addr = hosp_addr
        self.hosp_spec_empanl = hosp_spec_empanl
        self.hosp_spec_upgraded = hosp_spec_upgraded
        self.hosp_contact_no = hosp_contact_no
        self.hosp_contact_mail = hosp_contact_mail
        self.hosp_type = hosp_type

    def __repr__(self):
        return str(str(self.hosp_name))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uuid = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    aadhar = db.Column(db.Integer(), nullable=False, unique=True)
    addr = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False, unique=True)
    bld_donation = db.Column(db.Boolean(), nullable=False)
    age = db.Column(db.Integer(), nullable=True)
    bld_grp = db.Column(db.String(5), nullable=True)
    po_num = db.Column(db.Integer(), nullable=True)
    organ_donation = db.Column(db.Boolean(), nullable=False)
    pan = db.Column(db.String(10), nullable=True, unique=True)
    role = db.Column(db.Integer(), nullable=False, default=2)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return 'commit-success'

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
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def reset_password(cls, username, new_password):
        user = User.find_by_username(username=username)
        user.password = new_password
        user.save_to_db()

    def __init__(self, username, email, password, pan, name, sex, dob, bld_grp, addr, state, po_num, mobile, aadhar,
                 organ_donation, bld_donaton, city, age, role):
        self.uuid = str(uuid4())
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
        self.role = role


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(50), unique=True)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(uuid=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, name):
        self.uuid = str(uuid4())
        self.name = name


def __init__(self, **kwargs):
    for key, value in kwargs.items():
        setattr(self, key, value)


if __name__ == "__main__":
    # run migrate
    # manager.run()
    db.create_all()
