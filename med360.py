from datetime import date

import requests
from flask_admin import Admin

from models import db, app, User, City, Role, Scheme

admin = Admin(app, name='Med360')


def get_scheme_data():
    import pandas as pd
    schemes_file = r'../kb/scheme_hosp.txt'
    return pd.read_csv(open(schemes_file, 'r'), delimiter='\t')


def get_all_states_for_donors():
    return [(r[0], r[0]) for r in db.session.query(User.state).distinct()]


def get_all_states():
    states = [(r[0], r[0]) for r in db.session.query(City.state).distinct()]
    states.append(("None", "States"))
    return states


def get_all_roles():
    return [(r[0], r[1]) for r in db.session.query(Role.id, Role.name).distinct()]


def get_all_schemes():
    return [(r[0], r[1]) for r in db.session.query(Scheme.id, Scheme.name).distinct()]


def spec_code_dict():
    import pandas as pd
    codes = pd.read_csv('kb/codes.csv')
    codes.index = codes.code
    codes = codes.drop('code', axis=1)
    code_dict = []
    for i, j in codes.iterrows():
        if len(code_dict) == 0:
            code_dict.append(('None', 'Specialities'))
        code_dict.append((j.name, j.spec))
    return code_dict


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


def get_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def covid_data():
    corona_api_key = "f4491b20c4mshe066c8a643cdf41p1d21dfjsna43b3402be92"
    url = "https://covid-19-data.p.rapidapi.com/country"
    querystring = {"format": "json", "name": "india"}
    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': corona_api_key
    }

    global_url = 'https://api.covid19api.com/summary'
    global_resp = requests.request("GET", global_url)
    response = requests.request("GET", url, headers=headers, params=querystring)
    india_val = response.json()
    global_val = global_resp.json()
    return india_val, global_val


def distinct(input_list):
    if not isinstance(input_list, list):
        raise TypeError('Input has to be set to list type')
    seen_uuid = []
    final_out = []
    ids = [i.uuid for i in input_list]
    for obj in input_list:
        if ids.count(obj.uuid) == 1 or obj.uuid not in seen_uuid:
            final_out.append(obj)
            seen_uuid.append(obj.uuid)
    return final_out

# class Security:
#     __key = b'aT_s_1b8FBAD_mGTxAkJ3RvUlfrSJCQ1ewYHqFV58Vg='
#
#     @classmethod
#     def encrypt(cls, plain):
#         f = Fernet(cls.__key)
#         return f.encrypt(plain.encode("utf-8")).decode("utf-8")
#
#     @classmethod
#     def decrypt(cls, encrypted):
#         f = Fernet(cls.__key)
#         return f.decrypt(encrypted.encode("utf-8")).decode("utf-8")
#
#     def __init__(self, __key):
#         self.__key = __key
