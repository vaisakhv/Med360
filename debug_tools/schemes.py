import pandas as pd

from models import Hospital

schemes_file = r'../kb/scheme_hosp.txt'

file = pd.read_csv(open(schemes_file, 'r'), delimiter='\t')


def find_match():
    for i in file.iterrows():
        name = str(i[1]['hosp_name']).split(',')[0]
        out = Hospital.find_by_name(_name=name)
        out = out.order_by(Hospital.hosp_name).all()
        found = False
        if out:
            for one_id in out:
                if str(str(i[1]['hosp_name']).split(',')[-1]).upper() in one_id.hosp_addr:
                    print('sor')
                    print('\t', one_id.hosp_id, one_id.hosp_name, one_id.hosp_addr)
                    found = True
                    print('eor')
        # if found is not True:
        #     second_half = str(str(i[1]['hosp_name']).split(',')[1:]).upper()
        #     second_half = second_half.strip("[']")
        #     if ', ' in second_half:
        #         second_half = second_half.replace("', '", '')
        #     newList = Hospital.find_by_addr(second_half)
        #     new = newList.order_by(Hospital.hosp_addr).all()
        #     for one_hosp_frm_addr in new:
        #         print('++++++++++++++++++++++++++++++++++')
        #         print(one_hosp_frm_addr.hosp_name, ' || ', name)
        #         print('++++++++++++++++++++++++++++++++++')


if __name__ == '__main__':
    find_match()
