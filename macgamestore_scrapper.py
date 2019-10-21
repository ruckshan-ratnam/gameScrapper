import requests
import sqlite3

# Connect to our database
connection = sqlite3.connect('macPrices.db')
# Make our cursor
c = connection.cursor()

def insert_into_db(game_name,game_link,game_price):
    c.execute("INSERT INTO prices (gameName, price, link) VALUES (?,?,?)",
    (game_name, game_price, game_link))
    connection.commit()

url = "https://www.macgamestore.com/affiliate/feeds/p_F2E2D4.json"

r = requests.get(url)

data = r.json()

for i in data:
    insert_into_db(i['title'], i['current_price'], i['url'])

c.close()
connection.close()