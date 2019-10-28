import sqlite3

# Connect to all the databases
gog = sqlite3.connect('gogPrices.db')
gogCursor = gog.cursor()
gogCursor.execute('SELECT * FROM prices')
gogData = gogCursor.fetchall()

gameBillet = sqlite3.connect('gamebillet_database.db')
billetCursor = gameBillet.cursor()
billetCursor.execute('SELECT * FROM prices')
billetData = billetCursor.fetchall()

humble = sqlite3.connect('humble_bundle.db')
humbleCursor = humble.cursor()
humbleCursor.execute('SELECT * FROM prices')
humbleData = humbleCursor.fetchall()

macStore = sqlite3.connect('mac_store_database.db')
macCursor = macStore.cursor()
macCursor.execute('SELECT * FROM prices')
macData = macCursor.fetchall()

steam = sqlite3.connect('steam_prices.db')
steamCursor = steam.cursor()
steamCursor.execute('SELECT * FROM prices')
steamData = steamCursor.fetchall()



# Add all games to the each store set
gog_games = set(())
game_billet_games = set(())
humble_bundle_games = set(())
mac_store_games = set(())
steam_games = set(())

for i in gogData:
    gog_games.add(i[0])
for i in billetData:
    game_billet_games.add(i[0])
for i in humbleData:
    humble_bundle_games.add(i[0])
for i in macData:
    mac_store_games.add(i[0])
for i in steamData:
    steam_games.add(i[0])

# Union all the sets together and turn into a list and sort in alph order
all_games_alph = (list(set().union(gog_games,game_billet_games,humble_bundle_games,mac_store_games,steam_games))).sort()
