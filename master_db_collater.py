import sqlite3
import json
from database_helper import config,connect,insert,delete,update

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
all_games_alph = list(set().union(gog_games,game_billet_games,humble_bundle_games,mac_store_games,steam_games))
all_games_alph.sort()
with open('game_list.json','w',encoding='utf-8') as f:
    json.dump(all_games_alph,f,indent=4)

# add all games to the digital ocean db
sql_select_query = """SELECT * FROM prices WHERE gameName = ?"""
digital_ocean_games_db = connect()
master_db_cursor = digital_ocean_games_db.cursor()
for i in all_games_alph:
    gogCursor.execute(sql_select_query, (i,))
    billetCursor.execute(sql_select_query, (i,))
    humbleCursor.execute(sql_select_query, (i,))
    macCursor.execute(sql_select_query, (i,))
    steamCursor.execute(sql_select_query, (i,))

    gog_name = gogCursor.fetchone()
    mac_name = macCursor.fetchone()
    billet_name = billetCursor.fetchone()
    humble_name = humbleCursor.fetchone()
    steam_name = steamCursor.fetchone()

    insert(digital_ocean_games_db)
    digital_ocean_games_db.commit()

    if gog_name is not None:
        master_db_cursor.execute("UPDATE prices SET gog_price = %s WHERE gameName = %s",(gog_name[2],i))
        master_db_cursor.execute("UPDATE prices SET gog_link = %s WHERE gameName = %s",(gog_name[1],i))
        digital_ocean_games_db.commit()
    if mac_name is not None:
        master_db_cursor.execute("UPDATE prices SET mac_price = %s WHERE gameName = %s",(mac_name[2],i))
        master_db_cursor.execute("UPDATE prices SET mac_link = %s WHERE gameName = %s",(mac_name[1],i))
        digital_ocean_games_db.commit()
    if billet_name is not None:
        master_db_cursor.execute("UPDATE prices SET billet_price = %s WHERE gameName = %s",(billet_name[2],i))
        master_db_cursor.execute("UPDATE prices SET billet_link = %s WHERE gameName = %s",(billet_name[1],i))
        digital_ocean_games_db.commit()
    if humble_name is not None:
        master_db_cursor.execute("UPDATE prices SET humble_price = %s WHERE gameName = %s",(humble_name[2],i))
        master_db_cursor.execute("UPDATE prices SET humble_link = %s WHERE gameName = %s",(humble_name[1],i))
        digital_ocean_games_db.commit()
    if steam_name is not None:
        master_db_cursor.execute("UPDATE prices SET steam_price = %s WHERE gameName = %s",(steam_name[2],i))
        master_db_cursor.execute("UPDATE prices SET steam_link = %s WHERE gameName = %s",(steam_name[1],i))
        digital_ocean_games_db.commit()



# # Add all games to the master database
# master_database_connection = sqlite3.connect('master_database.db')
# master_db_cursor = master_database_connection.cursor()
# master_db_cursor.execute("CREATE TABLE IF NOT EXISTS prices(gameName TEXT, gogPrice TEXT, gogLink TEXT, macPrice TEXT, macLink TEXT, billetPrice TEXT, billetLink TEXT, humblePrice TEXT, humbleLink TEXT, steamPrice TEXT, steamLink TEXT)")
# # master_db_cursor.execute("INSERT INTO prices VALUES('gameName','0.00','https...','0.00','https...','0.00','https...','0.00','https...','0.00','https...')")
# master_database_connection.commit()

# sql_select_query = """SELECT * FROM prices WHERE gameName = ?"""
# print("started")
# for i in all_games_alph:
#     gogCursor.execute(sql_select_query, (i,))
#     billetCursor.execute(sql_select_query, (i,))
#     humbleCursor.execute(sql_select_query, (i,))
#     macCursor.execute(sql_select_query, (i,))
#     steamCursor.execute(sql_select_query, (i,))

#     gog_name = gogCursor.fetchone()
#     mac_name = macCursor.fetchone()
#     billet_name = billetCursor.fetchone()
#     humble_name = humbleCursor.fetchone()
#     steam_name = steamCursor.fetchone()
    
#     master_db_cursor.execute("INSERT INTO prices (gameName, gogPrice, gogLink, macPrice, macLink, billetPrice, billetLink, humblePrice, humbleLink, steamPrice, steamLink) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(i, "none", "none", "none", "none", "none","none", "none", "none", "none", "none"))
#     master_database_connection.commit()

#     if gog_name is not None:
#         master_db_cursor.execute("UPDATE prices SET gogPrice = ? WHERE gameName = ?",(gog_name[2],i))
#         master_db_cursor.execute("UPDATE prices SET gogLink = ? WHERE gameName = ?",(gog_name[1],i))
#         master_database_connection.commit()
#     if mac_name is not None:
#         master_db_cursor.execute("UPDATE prices SET macPrice = ? WHERE gameName = ?",(mac_name[2],i))
#         master_db_cursor.execute("UPDATE prices SET macLink = ? WHERE gameName = ?",(mac_name[1],i))
#         master_database_connection.commit()
#     if billet_name is not None:
#         master_db_cursor.execute("UPDATE prices SET billetPrice = ? WHERE gameName = ?",(billet_name[2],i))
#         master_db_cursor.execute("UPDATE prices SET billetLink = ? WHERE gameName = ?",(billet_name[1],i))
#         master_database_connection.commit()
#     if humble_name is not None:
#         master_db_cursor.execute("UPDATE prices SET humblePrice = ? WHERE gameName = ?",(humble_name[2],i))
#         master_db_cursor.execute("UPDATE prices SET humbleLink = ? WHERE gameName = ?",(humble_name[1],i))
#         master_database_connection.commit()
#     if steam_name is not None:
#         master_db_cursor.execute("UPDATE prices SET steamPrice = ? WHERE gameName = ?",(steam_name[2],i))
#         master_db_cursor.execute("UPDATE prices SET steamLink = ? WHERE gameName = ?",(steam_name[1],i))
#         master_database_connection.commit()

# Close all cursors
master_db_cursor.close()
gogCursor.close()
billetCursor.close()
humbleCursor.close()
macCursor.close()
steamCursor.close()

# Close all connections 
digital_ocean_games_db.close()
gog.close()
gameBillet.close()
humble.close()
macStore.close()
steam.close()

print("done")