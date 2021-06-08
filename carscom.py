import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

year_list = list()
make_list = list()
price_list = list()
body_style_list = list()
MPG_list = list()
seats_list = list()

html_page = requests.get(r"https://www.cars.com/research/sports/?catId=448&rn=0&rpp=13")
soup = BeautifulSoup(html_page.text, 'html.parser')
link = soup.find('a', attrs= {"cars-tracking-omniture-standard" : "Model Details"})

get_link = link.get("href")
link_page = requests.get(r"https://www.cars.com%s" %(get_link))
soup_link = BeautifulSoup(link_page.text, 'html.parser')

information_make = soup_link.find_all('h1', attrs= {"class" : "cui-page-section__title"})
information_price = soup_link.find_all('div', attrs= {"class" : "mmy-header__msrp mmy-header__info-border"})
information_some = soup_link.find_all('div', attrs= {"class" : "list-specs__value"})

for make in information_make:
    m_re = re.sub(r"\s+", " ", make.text)
    year = m_re.strip().split()[0]
    make = " ".join(m_re.strip().split()[1:])
    year_list.append(year)
    make_list.append(make)

for price in information_price:
    p_re = re.sub(r"\s+", " ", price.text)
    price_list.append(" ".join(p_re.strip().split()[0:3]))

some_list = list()

for some in information_some:
    s_re = re.sub(r"\s+", " ", some.text).strip()
    some_list.append(s_re)

body_style, seats, MPG = some_list

body_style_list.append(body_style)
seats_list.append(seats)
MPG_list.append(MPG)

data = {
    "(Year)" : year_list,
    "(Make)" : make_list,
    "(Body Style)" : body_style_list,
    "(Seats)" : seats_list,
    "(MPG)" : MPG_list,
    "(Price)" : price_list
}

df = pd.DataFrame(data)
print(df)