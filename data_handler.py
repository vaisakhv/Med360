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
    from views import City

    states_dist = pd.read_csv('sates_dist.csv', delimiter=',')
    states_dist.index = states_dist.State
    states_dist = states_dist.drop('State', axis=1)
    dists = states_dist._get_value('Tamil Nadu', col='District').split('\t')
    i = 14
    for dist in dists:
        city = City(id=i, state='Tamil Nadu', name=dist)
        city.save_to_db()
        i += 1


def addHospitals():
    from views import Hospital
    hospitals = pd.DataFrame()
    hospitals = hospitals.append(pd.read_csv('kerala_hospitals.csv'))
    hospitals = hospitals.append(pd.read_csv('tamilnadu_hospitals.csv'))
    hospitals.index = hospitals.Sno
    hospitals = hospitals.drop('Sno', axis=1)
    hospitals = hospitals.drop('Unnamed: 0', axis=1)
    cols = ['Hospital Name', 'Hospital Type', 'Hospital Address', 'Hospital E-Mail',
            'Hospital Contact', 'Specialities Empanelled', 'Specialities Upgraded']

    for i, row in hospitals.iterrows():
        new_hosp = Hospital(hosp_name=cleanVal(row['Hospital Name']), hosp_type=cleanVal(row['Hospital Type']),
                            hosp_addr=cleanVal(row['Hospital Address']),
                            hosp_contact_mail=cleanVal(row['Hospital E-Mail']),
                            hosp_contact_no=cleanVal(row['Hospital Contact']),
                            hosp_spec_empanl=cleanVal(row['Specialities Empanelled']),
                            hosp_spec_upgraded=cleanVal(row['Specialities Upgraded']))
        new_hosp.save_to_db()


def getCities(state):
    from views import City
    out = City.find_city_by_state('Kerala')
    return out


if __name__ == '__main__':
    # addHospitals()
    # addCities()
    print(getCities("Kerala"))
