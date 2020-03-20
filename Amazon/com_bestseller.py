import requests
from bs4 import BeautifulSoup
import os

Names = ["Not Available" for x in range(100)]
URLs = ["Not Available" for x in range(100)]
Authors = ["Not Available" for x in range(100)]
Prices = ["Not Available" for x in range(100)]
Num_Ratings = ["Not Available" for x in range(100)]
Avg_Ratings = ["Not Available" for x in range(100)]
Book_types = ["Not Available" for x in range(100)]


def amazon_scraper():
    ind = 0
    for page in range(1, 6):
        url = 'https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/' \
              'ref=zg_bs_pg_?' + str(page) + '_page_encoding=UTF8&pg=' + \
              str(page) + '&ajax=1'

        try:
            page_source = requests.get(url)
        except Exception as e:
            print(e)
            exit

        plain_text = page_source.text
        soup = BeautifulSoup(plain_text, "lxml")

        for book_type in soup.findAll('span', {'class': 'a-size-small '
                                                        'a-color-secondary'}):
            if book_type.string not in Book_types:
                Book_types.append(book_type.string)

        for data in soup.findAll('div', {'class': 'zg_itemWrapper'}):
            for book in data.findAll('div', {'class': 'p13n-sc-truncate '
                                                      'p13n-sc-line-clamp-1'}):
                Names[ind] = book.string.replace('\n', '').replace(',', '').\
                    replace(';', '')

            for link in data.findAll('a', {'class': 'a-link-normal '
                                                    'a-text-normal'}):
                href = "https://www.amazon.com/" + link.get('href')
                URLs[ind] = href.replace(',', '')

            for author in data.findAll('div', {'class': 'a-row a-size-small'}):
                if author.string not in Book_types:
                    Authors[ind] = author.string

            for price in data.findAll('span', {'class': 'p13n-sc-price'}):
                Prices[ind] = price.string

            for ratings in data.findAll('a', {'class':
                                        'a-size-small a-link-normal'}):
                Num_Ratings[ind] = ratings.string.replace(',', '')

            for average_rating in data.findAll('a',
                                               {'class': 'a-link-normal'}):
                average_rating = average_rating.get('title')
                if average_rating is not None:
                    Avg_Ratings[ind] = average_rating

            ind += 1

        page += 1
    return ind


def display(Num_Books):
    for i in range(Num_Books):
        print(i, Names[i], URLs[i], Authors[i], Prices[i], Num_Ratings[i],
              Avg_Ratings[i])


Num_Books = amazon_scraper()

try:
    Output_File = open('./output/com_book.csv', 'w')
except:
    os.system("mkdir output")
    Output_File = open('./output/com_book.csv', 'w')
Output_File.write("Name; URL; Author; Price; Number of Ratings; "
                  "Average Rating\n")
for i in range(Num_Books):
    Output_File.write(str(Names[i]) + ";" + str(URLs[i]) + ";" +
                      str(Authors[i]) + ";" + str(Prices[i]) + ";" +
                      str(Num_Ratings[i]) + ";" + str(Avg_Ratings[i]) + "\n")
Output_File.close()
