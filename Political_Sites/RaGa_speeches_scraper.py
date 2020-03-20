import requests
from bs4 import BeautifulSoup
import os
import pdftotext
init_notebook_mode(connected=True)

main_url = "https://www.inc.in/en/media/speeches"
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

dates = []
speeches = []


def scraper():
    for page in range(1, 8):
        url = main_url + "?page=" + str(page)
        try:
            page_source = requests.get(url, headers=agent)
        except Exception as e:
            print(e)
            exit

        plain_text = page_source.text
        soup = BeautifulSoup(plain_text, 'html.parser')

        required_speeches = soup.find("ul", {"class": "releases-list"})
        speeches = required_speeches.findAll("li")
        for speech in speeches:
            try:
                link = "https://www.inc.in/" + speech.find("a", {"class": "default-color"})['href']
                try:
                    speech_page = requests.get(link, headers=agent)
                except Exception as e:
                    print(e)
                    exit
                soup_page = BeautifulSoup(speech_page.text, 'html.parser')
                p_tags = soup_page.find_all("p")
                speech_link = p_tags[4].find("iframe")     
                
                if speech_link is None:
                    speech_tags = soup_page.find("div", {"class": "releases-list"}).find_all("span")
                    speech_data = ''
                    for speech_tag in speech_tags:
                        if speech_tag.string is not None:
                            speech_data += speech_tag.string
                    output_file.write(speech_data)      
                else: 
                    speech_link = speech_link['src']
                    try:
                        speech_tags = requests.get(speech_link, headers=agent)
                    except Exception as e:
                        print(e)
                        exit
                    
                    with open("temp.pdf", "wb") as f:
                        f.write(speech_tags.content)
                    with open("temp.pdf", "rb") as f:
                        pdf = pdftotext.PDF(f)
                    for page in pdf:
                        page = ' '.join(page.split()).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
                        page = ' '.join(page.split())
                        output_file.write(page)
                output_file.write("\n")
            except Exception as e:
                print(e)


output_file = open('RaGa_speeches.txt', 'a+')
scraper()
output_file.close()

f = open("RaGa_speeches.txt", "r")
content = f.read()
content = content.replace('.', ' ').replace(',', ' ').replace('(', ' ').replace(')', ' ').replace('।', ' ')
words = content.split()
final_content = []

for word in words:
    if len(word) > 3:
        final_content.append(word)

f = open("final_content.txt", "w")
for word in final_content:
    f.write("%s " % word)

