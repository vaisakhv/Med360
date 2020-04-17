import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import pandas as pd


pmjay_host = 'https://hospitals.pmjay.gov.in/Search/empnlWorkFlow.htm'
cols = ['Sno', 'Hospital Name', 'Hospital Type', 'Hospital Address', 'Hospital E-Mail', 'Hospital Contact',
        'Specialities Empanelled', 'Specialities Upgraded']
final_df = pd.DataFrame()
for page_html in range(233):
    appended_data = []
    req_params = {'actionFlag':  'ViewRegisteredHosptlsNew', 'search':  'Y', 'appReadOnly': 'Y', 'pageNo':  page_html,
                  'searchState': 33, 'searchDistrict': -1, 'searchHospType': -1, 'searchSpeciality': -1, 'noOfPages': 0}
    page = requests.get(url=pmjay_host, params=req_params)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    # print([len(T) for T in tr_elements[:12]]) len is 8
    col = []
    i = 0
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))

    for j in range(1, len(tr_elements)):
        # T is our j'th row
        T = tr_elements[j]

        # If row is not of size 8, the //tr data is not from our table
        if len(T) != 8:
            break

        # i is the index of our column
        i = 0

        # Iterate through each element of the row
        for t in T.iterchildren():
            data = t.text_content()
            # Check if row is empty
            if i > 0:
                # Convert any numerical value to integers
                try:
                    data = int(data)
                except:
                    pass
            # Append the data to the empty list of the i'th column
            col[i][1].append(data)
            # Increment i for the next column
            i += 1
        Dict = {title: column for (title, column) in col}
        df = pd.DataFrame(Dict)
        if len(df) is 10:
            appended_data.append(df)
            appended_data = pd.concat(appended_data)
    final_df = final_df.append(appended_data)
final_df = final_df.replace(r'\n', ' ', regex=True)
final_df = final_df.replace(r'\r', ' ', regex=True)
final_df = final_df.replace(r'\t', ' ', regex=True)
final_df.drop_duplicates(subset="Hospital Name", keep='last', inplace=True)
