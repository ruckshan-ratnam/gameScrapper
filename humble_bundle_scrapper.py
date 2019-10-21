from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sqlite3

inURL = "https://www.humblebundle.com/store/search?sort=bestselling&hmb_source=store_navbar"
pagesURL = "https://www.humblebundle.com/store/search?sort=bestselling&hmb_source=store_navbar&page="

page = 406

session = HTMLSession()
resp = session.get(inURL)
resp.html.render()

soup = BeautifulSoup(resp.html.html,'lxml')

names = []
prices = []
links = []

count = 0

while(count != page):
    session = HTMLSession()
    resp = session.get(pagesURL + str(count))
    resp.html.render()
    soup = BeautifulSoup(resp.html.html,'lxml')

    priceHolder = soup.find_all('span','price')
    nameHolder = soup.find_all('a','entity-link')
    linkHolder = soup.find_all('a','entity-link')

    for i in priceHolder:
        prices.append(i.text)

    for i in nameHolder:
        names.append(i['aria-label'])

    for i in linkHolder:
        links.append("https://www.humblebundle.com/store" + i['href'])
    
    count += 1


# Connect to our database
connection = sqlite3.connect('humble_bundle.db')
# Make our cursor
c = connection.cursor()

def insert_into_db(game_name,game_link,game_price):
    c.execute("INSERT INTO prices (gameName, price, link) VALUES (?,?,?)",
    (game_name, game_price, game_link))
    connection.commit()

count = 0

while(count != len(names)):
    insert_into_db(names[count], links[count], prices[count])

c.close()
connection.close()