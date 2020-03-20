import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
NUMBER_OF_PAGES = 13
pages = [str(i) for i in range(1,NUMBER_OF_PAGES)]
links = []

f= open("namo.txt","w+")

for page in pages:

    url = 'https://www.narendramodi.in/speech/loadspeeche?page=' + page + '&language=en'
    # sleep(0.5) Very Important
    sleep(randint(1,2))

    try:
        main_page = requests.get('https://www.narendramodi.in/speech/loadspeeche?page='+page+'&language=en',headers=agent)
    except Exception as e:
        print(e)
        exit
    
    soup = BeautifulSoup(main_page.text,'html.parser')

    divs = soup.findAll('div', class_ = 'speechImg left_class')

    for div in divs:
        anchor = div.find('a', class_ = 'left_class')
        link = anchor['href']
        # print(link)
        links.append(link)

# print(links)    

for link in links:

    print(link)
    sleep(randint(1,3))

    try:
        main_page = requests.get(link,headers=agent)
    except Exception as e:
        print(e)
        exit
    
    soup = BeautifulSoup(main_page.text,'html.parser')

    raw_content = soup.find('div', class_ = 'articleDetailsMain article_share_class')
    # print(raw_content)

    paras = raw_content.findAll('p')
    # print(paras)

    for para in paras:
        f.write(para.text)

    f.write("\n\n")

f.close() 




