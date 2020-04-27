from models import db, User, City


def get_all_states_for_donors():
    return [(r[0], r[0]) for r in db.session.query(User.state).distinct()]


def get_all_states():
    return [(r[0], r[0]) for r in db.session.query(City.state).distinct()]


def spec_code_dict():
    import pandas as pd
    codes = pd.read_csv('kb/codes.csv')
    codes.index = codes.code
    codes = codes.drop('code', axis=1)
    code_dict = []
    for i, j in codes.iterrows():
        if len(code_dict) == 0:
            code_dict.append(('None', 'Show all'))
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
