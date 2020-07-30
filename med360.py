import base64
from datetime import date

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from flask_admin import Admin

from models import db, app, User, City, Role, Scheme

admin = Admin(app, name='Med360')


def get_scheme_data():
    import pandas as pd
    schemes_file = r'../kb/scheme_hosp.txt'
    return pd.read_csv(open(schemes_file, 'r'), delimiter='\t')


def get_states_for_help():
    from pickle import load
    final_dist = load(open('kb/dist_list.pkl', 'rb'))
    return [(i, i) for i in final_dist]


def get_emergency_numbers(district):
    """
    :param district: district name
    :type district: str
    :return: two pd.df
    :rtype: pd.df
    """
    import pandas as pd
    helpline_pkl = r'kb/helpline.pkl'
    hotline_pkl = r'kb/hotline_numbers.pkl'
    helpline_df = pd.read_pickle(helpline_pkl)
    hotline_df = pd.read_pickle(hotline_pkl)
    hotline_result = hotline_df[hotline_df['District'].str.contains(district, case=False)]
    helpline_result = helpline_df[helpline_df['District'].str.contains(district, case=False)]
    return hotline_result, helpline_result


def get_all_states_for_donors():
    return [(r[0], r[0]) for r in db.session.query(User.state).distinct()]


def get_all_states():
    states = [(r[0], r[0]) for r in db.session.query(City.state).distinct()]
    states.append(("None", "States"))
    return states


def get_all_roles():
    return [(r[0], r[1]) for r in db.session.query(Role.id, Role.name).distinct()]


def get_all_schemes():
    return [(r[0], r[1]) for r in db.session.query(Scheme.uuid, Scheme.name).distinct()]


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


class Security:
    def encrypt(raw, __key):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        raw = base64.b64encode(pad(raw).encode('utf8'))
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key=__key[:16].encode('utf8'), mode=AES.MODE_CFB, iv=iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(enc, __key):
        unpad = lambda s: s[:-ord(s[-1:])]

        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(__key[:16].encode('utf8'), AES.MODE_CFB, iv)
        return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])))
