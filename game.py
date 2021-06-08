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

#game_id = "utah-royals-vs-portland-thorns-2019-09-06"
#game_id = "portland-thorns-vs-kansas-city-1-2021-04-09"
#boxscore_link = "http://api.nwslsoccer.com/v2/games/{}/stats".format(game_id)
#events_link = "http://api.nwslsoccer.com/v2/games/{}/commentary".format(game_id)
base_url =  "http://api.nwslsoccer.com/v2/games/"
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

def getChaosMetrics(game_id):
    events = getEvents(game_id)
    evetns_cnt = len(events)
    game = getGame(game_id)
    
    goals = game['liveData']['goal']
    goals_cnt = len(goals)

    cards = game['liveData']['card']
    cards_cnt = len(cards)

    length = game['liveData']['matchDetails']['matchLengthMin']

def getValue(values, tp):
    try:
        return float(values[tp])
    except:
        return 0

def getValue_dic(values, tp):
    try:
        return (values[tp])
    except:
        return 0
    
def generateActualChaos(chaos):
  stat = (chaos['cards_cnt'] 
          # + chaos['totalRedCard']
          + chaos['cornerTaken']
          + chaos['divingSave']
          + chaos['fouledFinalThird']
          + chaos['penAreaEntries']
          + chaos['totalShots']
          + chaos['passingAccuracy']
          + chaos['saves']
          + chaos['SOG']
          + chaos['shotFB']
          + chaos['totalGoals']
          + chaos['goalDif']
          )
  return stat  

class Game:
    
    def __init__(self, game_id):
        self.id = game_id
        
    def getPreGame(self):
        self._game = getGame(self.id) 
        self.matchid = self._game['matchInfo']['id']
        self.date = self._game['matchInfo']['date']
        self.time = self._game['matchInfo']['time']
        self.state = self._game['matchInfo']['location']['state']
        self.stadiumName = self._game['matchInfo']['location']['stadiumName']
        
        self.team0id = self._game['matchInfo']['contestant'][0]['team']['id']
        self.team0totalwins = self._game['matchInfo']['contestant'][0]['team']['winHistory']['totalMatchesWon']
        self.team0 = team.getTeamFromId(self.team0id)
    
        self.team1id = self._game['matchInfo']['contestant'][1]['team']['id']
        self.team1totalwins = self._game['matchInfo']['contestant'][1]['team']['winHistory']['totalMatchesWon']
        self.team1 = team.getTeamFromId(self.team1id)
    
    def getEvents(self):
        self._events = getEvents(self.id) # list of dic   
        self.events = pd.DataFrame(self._events)
        
    def getDetails(self):
        self._game = getGame(self.id)  
        self._liveData = self._game['liveData']
        self.broadcaster = self._liveData['broadcaster']['name'] # str
        self.cards = getValue_dic(self._liveData, 'card') # list of dic
        self.goals = getValue_dic(self._liveData, 'goal')# list of dic
        
        self._matchDetails = self._liveData['matchDetails']
        self.periodId = self._matchDetails['periodId']
        self.matchStatus = self._matchDetails['matchStatus']
        # self.winner = self._matchDetails['winner']
        self.matchLength = self._matchDetails['matchLengthMin'] + (self._matchDetails['matchLengthMin'])/60
        self._period = self._matchDetails['period']
        self._scores = self._matchDetails['scores']
        self.totalGoals = self._scores['total']['home'] + self._scores['total']['away']
        self.goalDif = abs(self._scores['total']['home'] - self._scores['total']['away'])
        
        self.ht = self._scores['ht']
        self.ft = self._scores['ft']
        self._lineUp = self._liveData['lineUp']
        
        # haven't though about these next ones
        self.missedPen = self._liveData['missedPen']
        self.penaltyShot = self._liveData['penaltyShot']
        self.substitute = self._liveData['penaltyShot']

    def getAdvancedStats(self):
        self._box = getBoxScore(self.id) # list of dic
        self._lineUp = self._box['lineUp']
        self._team1 = self._lineUp[0]
        self._team2 = self._lineUp[1]
        self.team1_stats = self._team1['stat']
        self.team2_stats = self._team1['stat']  
        self.team1_stats_df = pd.DataFrame(self._team1['stat'])
        self.team2_stats_df = pd.DataFrame(self._team2['stat'])
    
    def totalChaos(self):
        self.getAdvancedStats()
        self.getDetails()
        
        if self.cards == 0:
            cards_cnt = 0
        else:
            cards_cnt = len(self.cards)

        values1 = dict((temp['type'], temp['value']) for temp in self.team1_stats)
        values2 = dict((temp['type'], temp['value']) for temp in self.team2_stats)
        
        totalRedCard = getValue(values1, 'totalRedCard') + getValue(values2, 'totalRedCard')
        cornerTaken = getValue(values1, 'cornerTaken') + getValue(values2, 'cornerTaken')
        divingSave = getValue(values1, 'divingSave') + getValue(values2, 'divingSave')
        fouledFinalThird = getValue(values1, 'fouledFinalThird') + getValue(values2, 'fouledFinalThird')
        penAreaEntries = getValue(values1, 'penAreaEntries') + getValue(values2, 'penAreaEntries')
        totalShots = getValue(values1, 'totalShots') + getValue(values2, 'totalShots')
        passingAccuracy = getValue(values1, 'passingAccuracy') + getValue(values2, 'passingAccuracy')
        saves = getValue(values1, 'saves') + getValue(values2, 'saves')
        SOG = getValue(values1, 'shotsOnGoal') + getValue(values2, 'shotsOnGoal')
        shotFB = getValue(values1, 'shotFastbreak') + getValue(values2, 'shotFastbreak')
        
        dic = {
            'game id': self.id,
            'cards_cnt': cards_cnt,
            'totalRedCard': totalRedCard,
            'cornerTaken': cornerTaken,
            'divingSave': divingSave,
            'fouledFinalThird': fouledFinalThird,
            'penAreaEntries': penAreaEntries,
            'totalShots': totalShots,
            'passingAccuracy': passingAccuracy,
            'saves': saves,
            'SOG': SOG,
            'shotFB': shotFB,
            'totalGoals': self.totalGoals,
            'goalDif': self.goalDif
            }
        
        return dic
        

###MAIN

# "portland-thorns-vs-kansas-city-1-2021-04-09"
#game_id = "utah-royals-vs-washington-spirit-2019-04-20"
#game_id = "ol-reign-vs-chicago-red-stars-2021-04-27"
#game_id = "utah-royals-vs-portland-thorns-2019-09-06"
#game_id = "portland-thorns-vs-chicago-red-stars-2020-07-01"
game_id = "racing-louisville-vs-kansas-city-1-2021-05-15"
cursed = Game(game_id)
cursed.getPreGame()
# lineup = cursed._lineUp
# t1 = cursed._team1['stat']
# df_t1 = pd.DataFrame(t1)

cursed.getEvents()



chaos = cursed.totalChaos()

# stat = (chaos['cards_cnt'] 
#     + chaos['totalRedCard']
#     + chaos['cornerTaken']
#     + chaos['divingSave']
#     + chaos['fouledFinalThird']
#     + chaos['penAreaEntries']
#     + chaos['totalShots']
#     + chaos['passingAccuracy']
#     + chaos['saves']
#     + chaos['SOG']
#     + chaos['shotFB']
#     + chaos['totalGoals']
#     + chaos['goalDif']
#     )
# print(chaos)
# print(stat)
# y = {chaos['game id']: stat}

