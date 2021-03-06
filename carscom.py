import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

year_list = list()
make_list = list()
model_list = list()
price_list = list()
body_style_list = list()
MPG_list = list()
seats_list = list()

for page in (0,26,13):
    html_page = requests.get(r"https://www.cars.com/research/sports/?catId=448&rn=%i&rpp=13" %(page))
    
    soup = BeautifulSoup(html_page.text, 'html.parser')
    links = soup.find_all('a', attrs= {"cars-tracking-omniture-standard" : "Model Details"})

    for link in links:
        get_link = link.get("href")
        link_page = requests.get(r"https://www.cars.com%s" %(get_link))
        soup_link = BeautifulSoup(link_page.text, 'html.parser')

        # MAKE
        information_title = soup_link.find_all('a', attrs= {"data-linkname" : "bc-make"})

        for title in information_title:
            t_re = re.sub(r"\s+", " ", title.text)
            make_list.append(t_re.strip())

        # MODEL
        information_model = soup_link.find_all('a', attrs= {"cars-tracking-omniture-standard" : "bc-model"})

        for model in information_model:
            mo_re = re.sub(r"\s+", " ", model.text)
            model_list.append(mo_re.strip())

        # YRAES
        information_make = soup_link.find_all('h1', attrs= {"class" : "cui-page-section__title"})
    
        for make in information_make:
            m_re = re.sub(r"\s+", " ", make.text)
            year = m_re.strip().split()[0]
            #make = " ".join(m_re.strip().split()[1:])
            year_list.append(year)
            #make_list.append(make)
    
        #PRICE
        information_price = soup_link.find_all('div', attrs= {"class" : "mmy-header__msrp mmy-header__info-border"})

        for price in information_price:
            p_re = re.sub(r"\s+", " ", price.text)
            price_list.append(" ".join(p_re.strip().split()[0:3]))
    
        #3 info
        information_some = soup_link.find_all('div', attrs= {"class" : "list-specs__value"})

        some_list = list()

        for some in information_some:
            s_re = re.sub(r"\s+", " ", some.text).strip()
            some_list.append(s_re)

            if len(some_list) == 3:
                body_style, seats, MPG = some_list

                body_style_list.append(body_style)
                seats_list.append(seats.split()[0])
                MPG_list.append(MPG.split()[0])

#Creat a DataFrame
data = {
    "(Year)" : year_list,
    "(Make)" : make_list,
    "(Model)" : model_list,
    "(Body Style)" : body_style_list,
    "(Seats)" : seats_list,
    "(MPG)" : MPG_list,
    "(Price - MSRP)" : price_list
}

print(pd.DataFrame(data))