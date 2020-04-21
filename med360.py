from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)


def decodeSpecialties(spec):
    if 'NA' not in str(spec):
        import pandas as pd
        codes = pd.read_csv('kb/codes.csv')
        codes.index = codes.code
        codes = codes.drop('code', axis=1)
        specs = []
        if ',' in str(spec):
            spec = str(spec).replace(' ', '')
            spec = spec.split(',')
            for _spec in spec:
                specs.append(codes._get_value(_spec, col='spec'))
        else:
            specs.append(codes._get_value(spec.replace(' ', ''), col='spec'))
        return specs
    return ['NA']
