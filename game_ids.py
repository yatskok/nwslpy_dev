# -*- coding: utf-8 -*-
"""
Created on Mon May  3 18:28:36 2021

@author: yatsk
"""
import requests
import json
from bs4 import BeautifulSoup

import pandas as pd
import game as gm
games=[]

# 2020 Challenge Cup Scrape

base_url =  "https://www.nwslsoccer.com/schedule?season=2020%20Challenge%20Cup&"
def getGames(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    items = soup.find_all('div', class_="jsx-3742173839 c-match-item__button__wrapper")
    games = []
    for i in items:
        link = i.find('a')['href']
        link = link.split("/")[2]
        games.append(link)
    return games

games_rs19 = getGames("https://www.nwslsoccer.com/schedule?season=2019&")
games_cc20 = getGames("https://www.nwslsoccer.com/schedule?season=2020%20Challenge%20Cup&")
games_fs20 = getGames("https://www.nwslsoccer.com/schedule?season=2020%20Fall%20Series&")
games_cc21 = getGames("https://www.nwslsoccer.com/schedule?season=2021%20Challenge%20Cup&")
games_rs21 = getGames("https://www.nwslsoccer.com/schedule?season=2021&")

#%%
games = games_cc20 + games_fs20
game_stats = []
for game in games:
    game_ = gm.Game(game)
    game_stats.append(game_.totalChaos())
    
game_stats_df = pd.DataFrame(game_stats)
    
corl = game_stats_df.corr()

game_stats_df = game_stats_df.set_index('game id')

#%% Building response
descr = game_stats_df.describe()
#normalized_df1=(game_stats_df-game_stats_df.mean())/game_stats_df.std()
normalized_df=(game_stats_df-game_stats_df.min())/(game_stats_df.max()-game_stats_df.min())

def generateActualChaos(chaos):
  stat = (chaos['cards_cnt']*(1.9)
          # + chaos['totalRedCard']
          + chaos['cornerTaken']*(.5) #
          + chaos['divingSave']*(1.5) # 2
          + chaos['fouledFinalThird']*(.7)
          + chaos['penAreaEntries']*(.7) #
          + chaos['totalShots']*(1.3) # 2
          + chaos['passingAccuracy']*(.7)
          + chaos['saves']*(.7) #
          + chaos['SOG']*(1.3) # 2
          + chaos['shotFB']*(.7)
          + chaos['totalGoals']*(1.9)
          + chaos['goalDif']*(1.9)
          )
  return stat  

chaos_df = normalized_df.assign(chaos = generateActualChaos(normalized_df))


#%% 
games21 = games_rs21
game_stats21 = []
for game in games21:
    game_ = gm.Game(game)
    game_stats21.append(game_.getDetails())
    
game_stats_df21 = pd.DataFrame(game_stats21)
#%% POC modeling using 2020 games
import numpy as np
from sklearn.model_selection import train_test_split