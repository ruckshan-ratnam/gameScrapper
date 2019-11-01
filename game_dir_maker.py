import os
import json

game_names = []

with open('game_list.json','r') as r:
    game_names = json.load(r)


for i in game_names:
    if not os.path.exists(i):
        os.mkdir(i)