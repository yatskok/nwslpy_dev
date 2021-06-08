# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 19:42:20 2021

@author: yatsk
"""
import requests
import json
base_url =  "http://api.nwslsoccer.com/v2/teams/"

#2021
TEAMS = ['chicago-red-stars', 'houston-dash', 'kansas-city',
         'gotham-fc', 'north-carolina-courage', 'ol-reign',
         'orlando-pride', 'portland-thorns', 'racing-louiville']


def getTeamInfo(team):
    team_url = base_url + team
    r = requests.get(team_url)
    team_dic = r.json()['result']
#    json_formatted_str = json.dumps(r.json(), indent=2)
#    print(json_formatted_str)
    return team_dic
    
class Team:
    def __init__(self, slug):
        self._team = getTeamInfo(slug)
        self.slug = slug
        self.id = self._team['id']
        self.name = self._team['name']
        self.shortName = self._team['shortName']
        self.abbreviationName = self._team['abbreviationName']
        self.homeField = self._team['homeField']
        self.image = self._team['image']
        self.imageCredit = self._team['imageCredit']
        self.logo = self._team['logo']
        self.competitionId = self._team['competitionId']
        self.headCoach = self._team['headCoach']
        self.seasons = self._team['seasons']

def getID(team):
    dic = getTeamInfo(team)
    return dic['id']


def teamIDdic():
    dic = {}
    for t in TEAMS:
        team_url = base_url + t
        r = requests.get(team_url)
        if r.ok:
           tid = r.json()['result']['id']
           dic.update({str(tid): str(t)})
    return dic


def getTeams():
    r = requests.get(base_url)
    dic = {}
    if r.ok:
        teams = r.json()['result']
        for t in teams:
            try:
                dic.update({t['id']: t['slug']})
            except:
                t = None
    return dic

def getTeamFromId(tid):
    slug = getTeams()[tid]   
    return Team(slug)
    
# get
# teams = teamIDdic()[]
# ptfc = getTeamInfo("portland-thorns")

# ol_obj=Team("ol-reign")


# r = requests.get(base_url)
# if r.ok:
#     tesmp = r.json()['result']

# #teams_dic = teamIDdic()
# teams_dic = getTeam()