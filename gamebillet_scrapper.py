import requests
import sqlite3

url = "https://www.gamebillet.com/Product/JsonFeed?store=us&guid=596650DA-4E84-4857-9547-78B663616A34"

r = requests.get(url)

data = r.json()
products = data['product']

names = []
prices = []
links = []

for i in products:
    names.append(i['name'])
    prices.append(i['special_price'])
    links.append(i['url'] + "/?affiliate=f09c3ba0-355b-4ace-80d8-91edf2f7a8a3")


def insert_into_db(game_name,game_link,game_price):
    c.execute("INSERT INTO prices (gameName, price, link) VALUES (?,?,?)",
    (game_name, game_price, game_link))
    connection.commit()

# Connect to our database
connection = sqlite3.connect('gamebillet_database.db')
# Make our cursor
c = connection.cursor()

count = 0
while(count != len(names)):
    insert_into_db(names[count],links[count],prices[count])
    count += 1

c.close()
connection.close()