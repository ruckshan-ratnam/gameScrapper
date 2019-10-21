import requests
import sqlite3

# Connect to our database
connection = sqlite3.connect('gogPrices.db')
# Make our cursor
c = connection.cursor()

def insert_into_db(game_name,game_link,game_price):
    c.execute("INSERT INTO prices (gameName, price, link) VALUES (?,?,?)",
    (game_name, game_price, game_link))
    connection.commit()

url = "https://www.gog.com/games/ajax/filtered?mediaType=game&sort=title&page="

num_of_pages = 71

pages = []

for i in range(1, num_of_pages):
    r = requests.get(url + str(i))
    data = r.json()
    products = data['products']
    pages.append(products)

for i in pages:
    for x in i:
        insert_into_db(str(x['title']),str(x['price']['finalAmount']),str("https://www.gog.com"+ x['url']))


c.close()
connection.close()
