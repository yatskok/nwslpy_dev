# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:45:37 2021

@author: yatsk
"""
import requests
import pandas as pd
import team

TEAMS = team.getTeams()

#game_id = "utah-royals-vs-washington-spirit-2019-04-20"
#game_id = "ol-reign-vs-chicago-red-stars-2021-04-27"
game_id = "portland-thorns-vs-kansas-city-1-2021-04-09"
boxscore_link = "http://api.nwslsoccer.com/v2/games/{}/stats".format(game_id)
events_link = "http://api.nwslsoccer.com/v2/games/{}/commentary".format(game_id)
# SOME URL NOTES:
# 

def getEvents(game_id):
    events_link = base_url + game_id + "/commentary"
    r = requests.get(events_link)
    events_dic = r.json()['result']
    return events_dic
    #events_df = pd.DataFrame(events_dic)
    

def getBoxScore(game_id):
    boxscore_link = base_url + game_id + "/stats"
    r = requests.get(boxscore_link)    
    box_dic = r.json()['result']
    return box_dic


def getGame(game_id):   
    game_link = base_url + game_id
    r = requests.get(game_link)
    game_dic = r.json()['result']
    return game_dic
# box_df = pd.DataFrame(events_dic)

class Game:
    
    def __init__(self, game_id):
        self.id = game_id
        
    def getEvents(self):
        self._events = getEvents(self.id) # list of dic
    
    def getData(self):
    
    def getDetails(self):
        self._game = getGame(self.id)
        
        self._liveData = self._game['liveData']
        self.broadcaster = self._liveData['broadcaster']['name'] # str
        self.cards = self._liveData['card'] # list of dic
        self.goals = self._liveData['goal'] # list of dic
        
        self._matchDetails = self._liveData['matchDetails']
        self.periodId = self._matchDetails['periodId']
        self.matchStatus = self._matchDetails['matchStatus']
        self.winner = self._matchDetails['winner']
        self.matchLength = self._matchDetails['matchLengthMin'] + (self._matchDetails['matchLengthMin'])/60
        self._period = self._matchDetails['period']
        self._scores = self._matchDetails['scores']
        
        self._lineUp = self._liveData['lineUp']
        
        # haven't though about these next ones
        self.missedPen = self._liveData['missedPen']
        self.penaltyShot = self._liveData['penaltyShot']
        self.substitute = self._liveData['penaltyShot']

    def getAdvancedDetails(self):
        self._box = getBoxScore(game_id) # list of dic
        self.events = pd.DataFrame(self._events)
        self.cards = self._box['card'] # list of dic
        self.goals = self._box['goal'] # list of dic
        self._lineUp = self._box['lineUp']
        self._matchDetails = self._box['matchDetails']
        # haven't though about these next ones
        self.missedPen = self._box['missedPen']
        self.penaltyShot = self._box['penaltyShot']
        self.substitute = self._box['penaltyShot']
        
###MAIN

# cursed = Game(game_id)
# cursed.getDetails()
# lineup = cursed._lineUp

