import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to our database
connection = sqlite3.connect('steamPrices.db')
# Make our cursor
c = connection.cursor()

# Max ammount of pages at steam
PAGE_NUM = 2653

def steam_scrapper(page_num):

    # Make the lists to store everything
    game_titles = []
    game_links = []
    game_prices = []

    # Link to visit every page
    url_page = "https://store.steampowered.com/search/?page="

    # Keep track of the page we are on
    page = 1

    while(page != page_num):

        # Make the connection and the soup
        r = requests.get(url_page + str(page))
        soup = BeautifulSoup(r.text,'html.parser')

        try:
            # Get all the search items
            search_results = soup.find(id="search_resultsRows")

            # Look at all the titles
            titles = search_results.find_all("span","title")
            for i in titles:
                game_titles.append(i.text.strip())

            # Get all links to games
            links_to_games = search_results.find_all("a","search_result_row ds_collapse_flag")

            # Get all the links to the games
            for i in links_to_games:
                game_links.append(i['href'])


            # Get all the prices
            for i in links_to_games:
                try:
                    price = i.find("div","responsive_search_name_combined").find("div","col search_price responsive_secondrow").text.strip()
                    if len(price) is 0:
                        price = "no price found"
                    game_prices.append(price)
                except:
                    pass
        except:
            print("something went wrong when scrapping")
            pass

        page +=1
    
    return [game_titles,game_links,game_prices]


def data_entry(items):
    count = len(items[0])

    while(count != 0):
        try:
            game_name = items[0][count]
            game_link = items[1][count]
            game_price = items[2][count]
            data(game_name,game_link,game_price)
        except:
            pass
            print("something went wrong when getting the data from lists at " + str(count))
        count -= 1


def data(game_name,game_link,game_price):
    c.execute("INSERT INTO prices (gameName, price, link) VALUES (?,?,?)",
    (game_name, game_price, game_link))
    connection.commit()


items = steam_scrapper(PAGE_NUM)
data_entry(items)
c.close()
connection.close()