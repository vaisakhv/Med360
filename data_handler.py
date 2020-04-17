import pandas as pd
from app import Hospital

hospitals = pd.DataFrame()
hospitals = hospitals.append(pd.read_csv('kerala_hospitals.csv'))
hospitals = hospitals.append(pd.read_csv('tamilnadu_hospitals.csv'))
hospitals.index = hospitals.Sno
hospitals = hospitals.drop('Sno', axis=1)
hospitals = hospitals.drop('Unnamed: 0', axis=1)
cols = ['Hospital Name', 'Hospital Type', 'Hospital Address', 'Hospital E-Mail',
        'Hospital Contact', 'Specialities Empanelled', 'Specialities Upgraded']


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


for i, row in hospitals.iterrows():
    new_hosp = Hospital(hosp_name=cleanVal(row['Hospital Name']), hosp_type=cleanVal(row['Hospital Type']),
                        hosp_addr=cleanVal(row['Hospital Address']), hosp_contact_mail=cleanVal(row['Hospital E-Mail']),
                        hosp_contact_no=cleanVal(row['Hospital Contact']), hosp_spec_empanl=cleanVal(row['Specialities Empanelled']),
                        hosp_spec_upgraded=cleanVal(row['Specialities Upgraded']))
    new_hosp.save_to_db()
