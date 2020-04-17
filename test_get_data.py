import requests
from bs4 import BeautifulSoup

url_pagination = 'https://hospitals.pmjay.gov.in/Search/empnlWorkFlow.htm'

r = requests.get(url_pagination)
soup = BeautifulSoup(r.content, "html.parser")

page_url = "http://www.pour-les-personnes-agees.gouv.fr/annuaire-ehpad-en-hebergement-permanent/64/0?page={}"
last_page = soup.find('ul', class_='pagination').find('li', class_='next').a['href'].split('=')[1]
#last_page = soup.select_one('ul.pagination li.next a')['href'].split('=')[1] # with css selectors
dept_page_url = [page_url.format(i) for i in range(1, int(last_page)+1)]

print(dept_page_url)