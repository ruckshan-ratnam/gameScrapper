#!/bin/bash

clear

echo "making databases"

python3 create_gamebillet_database.py & python3 create_gog_database.py & python3 create_humble_bundle_database.py & python3 create_mac_game_store_database.py & python3 create_steam_database.py

echo "databases made"

echo "launching scrappers"

python3 gamebillet_scrapper.py & python3 gog_scrapper.py & python3 humble_bundle_scrapper.py & python3 macgamestore_scrapper.py & python3 steam_store_scrapper.py

echo "done scrapping"

echo "moving databses and scrapping files to database and scrapping folder"

mkdir database_scrapping
mv -t database_scrapping gamebillet_scrapper.py gog_scrapper.py humble_bundle_scrapper.py macgamestore_scrapper.py steam_store_scrapper.py master_db_collater.py
mv *.db database_scrapping

echo "merging databases into master databases"

python3 /database_scrapping/master_db_collater.py

echo "databases done"