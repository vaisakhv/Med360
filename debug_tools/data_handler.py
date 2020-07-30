import pandas as pd


def cleanVal(val):
    import re
    import numpy as np
    try:
        if not np.nan:
            return re.sub(' +', ' ', val)
        else:
            return val
    except Exception as e:
        print(type(val))


def addCities():
    from models import City

    states_dist = pd.read_csv('../kb/sates_dist.csv', delimiter=',')
    states_dist.index = states_dist.State
    states_dist = states_dist.drop('State', axis=1)
    dists = states_dist._get_value('Tamil Nadu', col='District').split('\t')
    i = 47
    for dist in dists:
        city = City(_id=i, _state='Tamil Nadu', _name=dist)
        city.save_to_db()
        i += 1


def add_hospitals():
    from models import Hospital

    hospitals = pd.DataFrame()
    hospitals = hospitals.append(pd.read_csv('../kb/kerala_hospitals.csv'))
    hospitals = hospitals.append(pd.read_csv('../kb/tamilnadu_hospitals.csv'))
    hospitals.index = hospitals.Sno
    hospitals = hospitals.drop('Sno', axis=1)
    hospitals = hospitals.drop('Unnamed: 0', axis=1)

    for i, row in hospitals.iterrows():
        new_hosp = Hospital(hosp_name=cleanVal(row['Hospital Name']), hosp_type=cleanVal(row['Hospital Type']),
                            hosp_addr=cleanVal(row['Hospital Address']),
                            hosp_contact_mail=cleanVal(row['Hospital E-Mail']),
                            hosp_contact_no=cleanVal(row['Hospital Contact']),
                            hosp_spec_empanl=cleanVal(row['Specialities Empanelled']),
                            hosp_spec_upgraded=cleanVal(row['Specialities Upgraded']))
        new_hosp.save_to_db()


def getCities(state):
    from models import City
    out = City.find_by_state('Kerala')
    return out


def load_schemes():
    file = 'kb/Medical_Scheme_details.txt'
    return pd.read_csv(open(file, 'r'), delimiter='\t')


def add_scheme_by_hosp_id(hosp_id, scheme_id):
    from models import Hospital, Scheme
    hosp = Hospital.find_by_id(int(hosp_id))
    scheme = Scheme.find_by_scheme_id(scheme_id)
    hosp.Schemes.append(scheme)
    hosp.save_to_db()


def convert_to_uuid(id):
    from models import Hospital
    hosp = Hospital.query.filter_by(hosp_id=id).first()
    return hosp.uuid


def add_schemes():
    from models import Scheme
    file = 'kb/Medical_Scheme_details.txt'
    schemes = pd.read_csv(open(file, 'r'), delimiter='\t')
    for i, row in schemes.iterrows():
        if i <= 11:
            new_scheme = Scheme(name=row['SCHEME NAME'], creator=row['GOVT TYPE'],
                                approved_states=row['STATE'], approved_districts=row['DISTRICT'],
                                feature=cleanVal(row['FEATURES']), objective=cleanVal(row['OBJECTUVE']),
                                benefits=cleanVal(row['BENEFIT COVER']), eligibility=cleanVal(row['ELIGIBILITY'])
                                )
            new_scheme.save_to_db()

