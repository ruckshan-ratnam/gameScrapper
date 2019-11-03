import os
import json

game_names = []
fails = []
with open('game_list.json','r') as r:
    game_names = json.load(r)


for i in game_names:
    try:
        if i is not None:
            if not os.path.exists(i):
                os.mkdir(i)
    except:
        fails.append(i)
        print('could not make dir for {}'.format(i))

with open('fails.json','w',encoding='utf-8') as f:
    json.dump(fails,f,indent=4)
    