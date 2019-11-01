import requests
from bs4 import BeautifulSoup
import json


url = "https://gamesdb.launchbox-app.com/games/results?id="

game_names = []

with open('game_list.json','r') as r:
    game_names = json.load(r)

for i in game_names:
    
    # Get the link to the game
    search = requests.get(url+game_names.replace(" ","%20"))
    link_to_game = (BeautifulSoup(search.text,'html.parser')).find("a","list-item")['href']
    
    # Go to that link
    game_url = "https://gamesdb.launchbox-app.com" + link_to_game
    r = requests.get(game_url)
    soup = BeautifulSoup(r.text,'html.parser')

    # Scrape all the rel datq
    data = soup.find_all("span","view")

    # Data is given in this order:
    # name, ignore, ignore, platform, release date, released, esrb rating, developer, publisher, genre, max players, co-op, ignore, ignore
    try:
        game_name = data[0].text
        platform = data[3].text
        release_date = data[4].text
        released = data[5].text
        esrb_rating = data[6].text
        developer = data[7].text.strip()
        publisher = data[8].text.strip()
        genre = data[9].text.strip()
        max_players = data[10].text
        co_op = data[11].text
    except:
        game_name = None
        platform = None
        release_date = None
        released = None
        esrb_rating = None
        developer = None
        publisher = None
        genre = None
        max_players = None
        co_op = None

    json_data = {
        "game" : game_name,
        "platform" : platform,
        "release date" : release_date,
        "released" : released,
        "esrb rating" : esrb_rating,
        "developer" : developer,
        "publisher" : publisher,
        "genre" : genre,
        "max players" : max_players,
        "co-op" : co_op
        }

    with open(i+'/'+json_data['game']+'.json', 'w', encoding='utf-8') as f:
        json.dump(json_data,f,indent=4)