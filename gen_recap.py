# NBA NLP - Senior Project - Spring 2015
# Recap Generator - Main
# Jacob Bustamante

"""
gen_recap
This is the main file which generates recap articles and calls importting and scraping functions.
"""

import sys, re, os, sqlite3, random, glob
import inspect
import recap_strings
from data import nba_db
from data import data_globals as dg
from scrapers import nba_scrapers
from scrapers import scrapers_globals as sg
from data.create_database import create_db


DEBUG = False
web_dir = "./web/2014_season/"

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Turns a number into its ordinal. ex) 2 -> 2nd, 5 -> 5th
num_ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

"""
Headline recap bidding
gen_headline is called, which runs each of the following bid functions.
The bid with the highest rating is chosen as the headline.
"""

bid_headline_counts = {'bid_headline_default':0, 'bid_headline_player':0, 'bid_last_second_shot':0, 'bid_headline_partial_default':0, 'bid_headline_tied_partial_default':0, 'bid_headline_comeback':0, 'bid_headline_team_rating':0}

def bid_headline_default(info):
    return (0.25, recap_string_from_list(recap_strings.headline_strings, info), 'bid_headline_default')

def bid_headline_player(info):
    global events
    headline = ""
    rating = 0
    stat = 17
    for event in events:
        if type(event.event) is Event_Stat and event.event.high and event.rating >= rating and event.event.player.points > stat:
            headline = event.event.gen_headline()
            rating = event.rating
            stat = event.event.player.points
    return (rating, headline, 'bid_headline_player')

def bid_headline_team_rating(info):
    global events
    headline = ""
    rating = 0
    for event in events:
        if type(event.event) is Event_Team_Rating and event.rating >= rating and event.event.players[0].team == info['winner_team_name']:
            headline = event.event.gen_headline()
            rating = event.rating
    return (rating, headline, 'bid_headline_team_rating')

def bid_last_second_shot(info):
    global events
    headline = ""
    rating = 0
    for event in events:
        if type(event.event) is Event_Last_Second_Shot and event.rating >= rating:
            headline = event.event.gen_headline()
            rating = event.rating
    return (rating, headline, 'bid_last_second_shot')

def bid_headline_comeback(info):
    global events
    headline = ""
    rating = 0
    for event in events:
        if type(event.event) is Event_Comeback and event.rating >= rating:
            headline = event.event.gen_headline()
            rating = event.rating
    return (rating, headline, 'bid_headline_comeback')

def bid_headline_partial_default(info):
    rating = 0.85 if partial else 0.0
    if rating:
        return (rating, recap_string_from_list(recap_strings.headline_partial_strings, info), 'bid_headline_partial_default')
    else:
        return (rating, "", 'bid_headline_partial_default')

def bid_headline_tied_partial_default(info):
    rating = 0.90 if partial and info['home_score'] == info['away_score'] else 0.0
    if rating:
        return (rating, recap_string_from_list(recap_strings.headline_tied_partial_strings, info), 'bid_headline_tied partial_default')
    else:
        return (rating, "", 'bid_headline_partial_default')


def gen_headline(info):
    output = []
    
    max_bid = max([globals()[bid_function](info) for bid_function in bid_headline_counts.keys()])
    output.append(max_bid[1])
    
    return output


"""
Record and standings recap
gen_record is called, which runs each of the following bid functions, separated into general and meta functions.
The general bid with the highest rating is chosen as the main record story.
All the meta bids rated above a 0 are chosen to follow the main story.
"""

bid_record_counts = {'bid_record_default':0, 'bid_record_partial_default':0}
bid_record_meta_counts = {'bid_record_history':0, 'bid_record_home_streak':0, 'bid_record_away_streak':0, 'bid_record_last_few':0}

def bid_record_default(info):
    return (0.25, recap_string_from_list(recap_strings.record_strings, info), 'bid_record_default')

def bid_record_partial_default(info):
    rating = 0.85 if partial else 0.0
    return (rating, recap_string_from_list(recap_strings.record_partial_strings, info), 'bid_record_partial_default')

def bid_record_history(info):
    rating = 0.0
    return (rating, recap_string_from_list(recap_strings.record_partial_strings, info), 'bid_record_history')

def bid_record_home_streak(info):
    game_id = int(info['game_id']) if not partial else int(info['game_id']) - 1
    return bid_record_streak(info['home_team_id'], game_id, info['home_team'])

def bid_record_away_streak(info):
    game_id = int(info['game_id']) if not partial else int(info['game_id']) - 1
    return bid_record_streak(info['away_team_id'], game_id, info['away_team'])

def bid_record_streak(team_id, game_id, team_name):
    games_wins_losses = nba_db.get_team_streak(team_id, game_id)
    d = {'num_past_games':games_wins_losses[0], 'num_won':games_wins_losses[1], 'num_loss':games_wins_losses[2], 'team_name':team_name}
    winning = games_wins_losses[1] > 0
    if games_wins_losses[0] == 0:
        rating = 0
        return (rating, "", 'bid_record_home_streak')
    elif winning:
        rating = (games_wins_losses[1] / 100) * 4
        if partial:
            return (rating, recap_string_from_list(recap_strings.team_winning_streak_partial_strings, d))
        else:
            return (rating, recap_string_from_list(recap_strings.team_winning_streak_strings, d))
    else:
        rating = (games_wins_losses[2] / 100) * 4
        if partial:
            return (rating, recap_string_from_list(recap_strings.team_losing_streak_strings, d))
        else:
            return (rating, recap_string_from_list(recap_strings.team_losing_streak_partial_strings, d))

def bid_record_last_few(info):
    rating = 0.0
    return (rating, recap_string_from_list(recap_strings.record_partial_strings, info), 'bid_record_last_few')

def gen_record(info):
    output = []
    
    max_bid = max([globals()[bid_function](info) for bid_function in bid_record_counts.keys()])
    output.append(max_bid[1])
    
    for bid in [globals()[bid_function](info) for bid_function in bid_record_meta_counts.keys()]:
        if bid[0] > 0:
            output.append(bid[1])
    
    return output


"""
Events
An Event is a data structure that holds data for a given event. Ex. High stats, last second shot, foul out.
These events have text generation functions that can generate strings based its event data.
Events can be added or removed by creating Event subclasses, if neccessary, and adding an even calculation
function to the calc_events function.
"""
class Event:
    def __init__(self, rating, event):
        self.rating = rating
        self.event = event
    
    def __repr__(self):
        return "{" + str(self.rating) + " : " + self.event.__repr__() + "}"
    
    def gen_string(self):
        return self.event.gen_string()
    
    def gen_story(self):
        return self.event.gen_story()
    
    def gen_summary(self):
        return self.event.gen_summary()

class Event_Stat:
    def __init__(self, player=None, high=False, leader=False):
        self.player = player
        self.team = player.team
        self.high = high
        self.leader = leader
        self.calc_details()
    
    def __repr__(self):
        return str(self.player) + " " + self.team
    
    def get_dict(self):
        d = dict()
        d['name'] = self.player.name
        d['team'] = self.player.team
        d['stat_name'] = "points"
        d['stat'] = self.player.points
        d['stat_noun'] = "scoring"
        d['points'] = self.player.points
        d.update(self.player.db.get_dict())
        return d
    
    def gen_headline(self):
        global game_info
        d = self.get_dict()
        d.update(game_info)
        if self.high:
            return recap_string_from_list(recap_strings.headline_high_rating_strings, d)
        elif self.leader:
            return recap_string_from_list(recap_strings.headline_high_rating_leader_strings, d)
        else:
            return recap_string_from_list(recap_strings.headline_stat_strings, d)
    
    def gen_summary(self):
        if self.high:
            return recap_string_from_list(recap_strings.intro_high_rating_strings, self.get_dict())
        elif self.leader:
            return recap_string_from_list(recap_strings.intro_high_rating_leader_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.intro_stat_strings, self.get_dict())
    
    def gen_string(self):
        if self.high:
            return recap_string_from_list(recap_strings.high_rating_strings, self.get_dict())
        elif self.leader:
            return recap_string_from_list(recap_strings.high_rating_leader_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.stat_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details = []
        self.details.append(self)
        event_details = Event_High_Rating_Details(self.player)
        event_quarter = Event_High_Rating_Quarter(self.player)
        if self.player and self.high:
            if event_details.rating > 0:
                self.details.append(event_details)
            if event_quarter.rating > 0:
                self.details.append(event_quarter)
        elif self.player and self.leader:
            if event_details.rating > 0:
                self.details.append(event_details)
            if event_quarter.rating > 0:
                self.details.append(event_quarter)
        elif self.player:
            #self.details.append(Event_High_Rating_Quarter(self.player))
            if event_details.rating > 0:
                self.details.append(event_details)

# TODOOOO
class Event_Team_Rating:
    def __init__(self, players=[], high=False, leader=False):
        self.players = players
        self.high = high
        self.leader = leader
        self.team = self.players[0].team
        self.total_points = sum([p.points for p in players])
        self.player = ", ".join([p.name for p in players[:-1]])
        self.player += (" and " + players[-1].name) if len(players) == 2 else (", and " + players[-1].name)
        if [p.points for p in players].count(players[0].points) == len(players):
            self.points = str(players[0].points) + " points each"
        else:
            self.points = ", ".join([str(p.points) for p in players[:-1]])
            self.points += (" and " + str(players[-1].points)) if len(players) == 2 else (", and " + str(players[-1].points))
            self.points += " points respectively"
        self.calc_details()
    
    def __repr__(self):
        return str(self.player) + " " + self.points
    
    def get_dict(self):
        d = dict()
        d['name'] = self.player
        d['team'] = self.players[0].team
        d['total_points'] = self.total_points
        d['points'] = self.points
        
        d['stat_name'] = "points"
        d['stat'] = self.points
        d['stat_noun'] = "scoring"
        
        # TODO 
        d.update(self.players[0].db.get_dict())
        return d
    
    def gen_headline(self):
        global game_info
        d = self.get_dict()
        d.update(game_info)
        if self.leader:
            return recap_string_from_list(recap_strings.headline_high_team_rating_strings, d)
        elif self.high:
            return recap_string_from_list(recap_strings.headline_high_team_rating_strings, d)
        else:
            return recap_string_from_list(recap_strings.headline_team_rating_strings, d)
    
    def gen_summary(self):
        if self.leader:
            return recap_string_from_list(recap_strings.intro_high_team_rating_strings, self.get_dict())
        elif self.high:
            return recap_string_from_list(recap_strings.intro_high_team_rating_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.intro_team_rating_strings, self.get_dict())
    
    def gen_string(self):
        if self.leader:
            return recap_string_from_list(recap_strings.high_team_rating_strings, self.get_dict())
        elif self.high:
            return recap_string_from_list(recap_strings.high_team_rating_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.team_rating_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details = []
        self.details.append(self)
        
        if self.leader:
            for p in self.players:
                event_details = Event_High_Rating_Details(p, self.high)
                event_quarter = Event_High_Rating_Quarter(p)
                if event_details.rating > 0:
                    self.details.append(event_details)
                if event_quarter.rating > 0:
                    self.details.append(event_quarter)
        elif self.high:
            for p in self.players:
                event_details = Event_High_Rating_Details(p, self.high)
                event_quarter = Event_High_Rating_Quarter(p)
                if event_details.rating > 0:
                    self.details.append(event_details)
                if event_quarter.rating > 0:
                    self.details.append(event_quarter)
        else:
            for p in self.players:
                event_details = Event_High_Rating_Details(p, self.high)
                if event_details.rating > 0:
                    self.details.append(event_details)


class Event_Scoring_Run:
    def __init__(self, team="", points=0, turnovers=0, missed_attempts=0, start_time=0, end_time=0):
        self.team = team
        self.points = points
        self.turnovers = turnovers
        self.missed_attempts = missed_attempts
        self.start_time = start_time
        self.end_time = end_time
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return self.team + " " + str(self.points) + " " + str(self.turnovers) + " " + str(self.start_time) + " " + str(self.end_time)
    
    def get_dict(self):
        global game_info
        
        d = dict()
        d['winning_team'] = self.team
        d['winning_points'] = self.points
        d['losing_team'] = [name for name in game_info['teams'] if name not in [self.team]][0]
        d['losing_points'] = 0
        d['turnovers'] = self.turnovers
        d['missed_attempts'] = self.missed_attempts
        d['s_quarter'] = self.start_time[0]
        d['s_minutes'] = self.start_time[1]
        d['s_seconds'] = self.start_time[2]
        d['e_quarter'] = self.end_time[0]
        d['e_minutes'] = self.end_time[1]
        d['e_seconds'] = self.end_time[2]
        return d
    
    def gen_summary(self):
        return recap_string_from_list(recap_strings.intro_run_strings, self.get_dict())
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.scoring_run_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)

class Event_High_Rating_Quarter:
    global partial, partial_time
    def __init__(self, player):
        self.player = player
        self.calc_high_quarter()
        self.rating = .5 if self.points >= self.player.points / 2 else 0
        if partial:
            if partial_time[0] < 3:
                self.rating = 0
            elif partial_time[0] == 3:
                self.rating = .5 if self.points >= self.player.points * .8 else 0
    
    def __repr__(self):
        return self.player.name + " " + self.quarter + " " + self.points
    
    def calc_high_quarter(self):
        quarter_x_points = list(enumerate([self.player.points_1, self.player.points_2, self.player.points_3, self.player.points_4], 1))
        high_q_x_p = max(quarter_x_points, key=lambda k:k[1])
        self.quarter, self.points = high_q_x_p
        
    def get_dict(self):
        global game_info
        
        d = self.player.get_dict()
        d['high_quarter'] = num_ordinal(self.quarter)
        d['high_quarter_points'] = self.points
        return d
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.high_rating_quarter_strings, self.get_dict())
    
    def gen_story(self):
        return None

class Event_High_Rating_Details:
    def __init__(self, player, high=False):
        self.player = player
        self.high = high
        self.rating = (player.assists / 100) + (player.rebounds / 100)
    
    def __repr__(self):
        return self.player.name + " " + self.player.assists + " " + self.player.rebounds
    
    def get_dict(self):
        global game_info
        
        d = self.player.get_dict()
        if self.player.assists and self.player.rebounds:
            d['assists_and_rebounds'] = str(self.player.assists) + " assists and " + str(self.player.rebounds) + " rebounds"
        elif self.player.assists:
            d['assists_and_rebounds'] = str(self.player.assists) + " assists"
        elif self.player.rebounds:
            d['assists_and_rebounds'] = str(self.player.rebounds) + " rebounds"
        return d
    
    def gen_string(self):
        if self.high:
            return recap_string_from_list(recap_strings.high_rating_details_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.stat_details_strings, self.get_dict())
    
    def gen_story(self):
        return None

class Event_Last_Second_Shot:
    def __init__(self, team="", points=0, time_left=0, primary_player="", shot_type=""):
        self.team = team
        self.points = points
        self.time_left = time_left
        self.primary_player = primary_player
        self.shot_type = shot_type
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return self.team + " " + str(self.points) + " " + str(self.time_left) + " " + str(self.primary_player)
    
    def get_dict(self):
        global game_info
        
        d = dict()
        d['winning_team'] = game_info['winner_team_name']
        d['points'] = self.points
        d['losing_team'] = game_info['loser_team_name']
        d['primary_player'] = self.primary_player
        d['winner_score'] = game_info['winner_score']
        d['loser_score'] = game_info['loser_score']
        d['shot_type'] = self.shot_type
        d['quarter'] = self.time_left[0]
        d['quarter_str'] = num_ordinal(self.time_left[0])
        d['minutes'] = self.time_left[1]
        d['seconds'] = self.time_left[2]
        return d
    
    def gen_headline(self):
        return recap_string_from_list(recap_strings.headline_last_second_shot_strings, self.get_dict())

    def gen_summary(self):
        return recap_string_from_list(recap_strings.intro_last_second_shot_strings, self.get_dict())
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.last_second_shot_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)

class Event_Big_Lead:
    def __init__(self, lead_team="", down_team="", lead_points=0, down_points=0, s_time=0):
        self.lead_team = lead_team
        self.down_team = down_team
        self.points_up = lead_points - down_points
        self.lead_points = lead_points
        self.down_points = down_points
        self.s_time = s_time
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return self.lead_team + " " + str(self.points_up) + " " + str(self.s_time)
    
    def get_dict(self):
        global game_info
        
        d = dict()
        d['lead_team'] = self.lead_team
        d['down_team'] = self.down_team
        d['points_up'] = self.points_up
        d['lead_points'] = self.lead_points
        d['down_points'] = self.down_points
        d['quarter'] = self.s_time[0]
        d['quarter_str'] = num_ordinal(self.s_time[0])
        d['minutes'] = self.s_time[1]
        d['seconds'] = self.s_time[2]
        return d
    
    def gen_summary(self):
        return recap_string_from_list(recap_strings.intro_big_lead_strings, self.get_dict())
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.big_lead_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)

class Event_High_Overall_Stats:
    def __init__(self, player=None):
        self.player = player
        self.team = player.team
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return str(self.player)
    
    def get_dict(self):
        d = dict()
        d['name'] = self.player.name
        d['team'] = self.player.team
        d['points'] = self.player.points
        d['assists'] = self.player.assists
        d['rebounds'] = self.player.rebounds
        d.update(self.player.db.get_dict())
        return d
    
    def gen_headline(self):
        global game_info
        d = self.get_dict()
        d.update(game_info)
        return recap_string_from_list(recap_strings.headline_overall_stats_strings, d)
    
    def gen_summary(self):
        return recap_string_from_list(recap_strings.intro_overall_stats_strings, self.get_dict())
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.overall_stats_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)
        if self.player:
            pass

class Event_Foul_Out:
    def __init__(self, player=None, time_left=(0,0,0)):
        self.player = player
        self.quarter = time_left[0]
        self.minutes = "%02d" % time_left[1]
        self.seconds = "%02d" % time_left[2]
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return str(self.player) + " " + str(self.quarter) + " " + str(self.minutes) + " " + str(self.seconds)
    
    def get_dict(self):
        global game_info
        
        d = self.player.get_dict()
        d['name'] = self.player.name
        d['quarter'] = self.quarter
        d['minutes'] = self.minutes
        d['seconds'] = self.seconds
        d['quarter_str'] = get_quarter_str(self.quarter)
        return d
    
    def gen_headline(self):
        return recap_string_from_list(recap_strings.headline_foul_out_strings, self.get_dict())
    
    def gen_summary(self):
        return recap_string_from_list(recap_strings.intro_foul_out_strings, self.get_dict())
    
    def gen_string(self):
        return recap_string_from_list(recap_strings.foul_out_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)

class Event_Comeback:
    def __init__(self, success=True, comeback_team=None, other_team=None, points_down=None, quarter_down=None, lead=None):
        self.success = success
        self.comeback_team = comeback_team
        self.other_team = other_team
        self.points_down = points_down
        self.quarter_down = quarter_down
        self.quarter_str = num_ordinal(quarter_down)
        self.lead = lead
        self.details = []
        self.calc_details()
    
    def __repr__(self):
        return str(self.comeback_team) + " " + str(self.other_team) + " " + str(self.points_down)
    
    def get_dict(self):
        d = dict()
        d['comeback_team'] = self.comeback_team.name
        d['other_team'] = self.other_team.name
        d['points_down'] = self.points_down
        d['quarter_down'] = self.quarter_down
        d['quarter_str'] = self.quarter_str
        d['lead'] = self.lead
        return d
    
    def gen_headline(self):
        global game_info
        d = self.get_dict()
        d.update(game_info)
        if self.success:
            return recap_string_from_list(recap_strings.headline_comeback_success_strings, d)
        else:
            return recap_string_from_list(recap_strings.headline_comeback_fail_strings, d)
    
    def gen_summary(self):
        if self.success:
            return recap_string_from_list(recap_strings.intro_comeback_success_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.intro_comeback_fail_strings, self.get_dict())
    
    def gen_string(self):
        if self.success:
            return recap_string_from_list(recap_strings.comeback_success_strings, self.get_dict())
        else:
            return recap_string_from_list(recap_strings.comeback_fail_strings, self.get_dict())
    
    def gen_story(self):
        return [detail.gen_string() for detail in self.details]
    
    def calc_details(self):
        self.details.append(self)

"""
Event Calc funtcions
These are the calc functions for events. These are the functions that discover events in the game data.
calc functions can be added by creating the function, then calling it in calc_events().
"""

def calc_high_stat_events():
    global events, players
    
    high_points = 17
    rating_cutoff = .25
    #high_points = 10
    
    for player in players.values():
        rating = 0.2 + (player.points / 100) * 2 + (player.assists / 100) + (player.rebounds / 100) + (player.blocks / 100) + (player.steals / 100)
        if player.points > high_points:
            #events.append(Event(rating, Event_High_Rating(player, 'points', player.points, 'scoring')))
            events.append(Event(rating, Event_Stat(player, high=True)))
        elif rating > rating_cutoff:
            events.append(Event(rating, Event_Stat(player)))
        

def calc_high_overall_stats_events():
    global events, players
    
    high_points = 19
    high_assists = 8
    high_rebounds = 10
    high_steals = 6
    high_blocks = 6
    
    for player in players.values():
        rating = 0
        if player.points > high_points:
            rating += 0.3
        if player.assists > high_assists:
            rating += 0.3
        if player.rebounds > high_rebounds:
            rating += 0.3
            
        if rating >= 0.6:
            events.append(Event(rating, Event_High_Overall_Stats(player)))

def calc_scoring_run():
    global events, game_info, game_plays
    
    # TODO: include some opposing points, maybe a 3 points cutoff
    
    high_run = 11
    run_team = ""
    run_points = 0
    turnovers = 0
    missed_attempts = 0
    start_time = (0,0,0)
    end_time = (0,0,0)
    
    for play_index, play in enumerate(game_plays):
        if play['play_type'] in ['shot', 'assist', 'blocks', 'free throw'] and play['shot_made'] == "makes":
            if play['name'] != run_team:
                if run_points > high_run:
                    end_time = (play['quarter_str'], play['minutes'], play['seconds'])
                    events.append(Event(0.5, Event_Scoring_Run(run_team, run_points, turnovers, missed_attempts, start_time, end_time)))
                run_points = 0
                turnovers = missed_attempts = 0
                run_team = play['name']
                start_time = (play['quarter_str'], play['minutes'], play['seconds'])
            # TODO
            if play['points_worth']:
                run_points += int(play['points_worth'])
        elif play['play_type'] in ['shot', 'assist', 'free throw'] and (play['shot_made'] == None or play['shot_made'] == "misses"):
            if play['name'] != run_team:
                missed_attempts += 1
        elif play['play_type'] in ['steal']:
            if play['name'] != run_team:
                turnovers += 1

def calc_last_second_shot():
    global events, game_info, game_plays
    
    # do if check for partial
    
    for play in reversed(game_plays):
        # gets last points
        # still need time cutoff
        if play['play_type'] in ['shot', 'assist', 'free throw'] and play['shot_made'] == "makes":
            time_left = (play['quarter'], play['minutes'], play['seconds'])
            if abs(play['home_score'] - play['away_score']) <= play['points_worth'] and time_left[1] == 0 and time_left[2] < 10:
                if play['home_score'] > play['away_score'] and play['name'] == game_info['home_team']:
                    time_left = (play['quarter'], play['minutes'], play['seconds'])
                    events.append(Event(0.95, Event_Last_Second_Shot(play['name'], play['points_worth'], time_left, play['primary_player'], play['shot_type'])))
                    break
                elif play['away_score'] > play['home_score'] and play['name'] == game_info['away_team']:
                    time_left = (play['quarter'], play['minutes'], play['seconds'])
                    events.append(Event(0.95, Event_Last_Second_Shot(play['name'], play['points_worth'], time_left, play['primary_player'], play['shot_type'])))
                    break
                else:
                    break
            else:
                break

def calc_big_lead():
    global events, game_info, game_plays
    
    biggest_lead_cutoff = 10
    
    biggest_lead = biggest_lead_cutoff
    for play in game_plays:
        cur_lead = abs(play['home_score'] - play['away_score'])
        if cur_lead > biggest_lead:
            biggest_lead = cur_lead
            time_s = (play['quarter'], play['minutes'], play['seconds'])
            if play['home_score'] > play['away_score']:
                lead_team = game_info['home_team']
                down_team = game_info['away_team']
                lead_points = play['home_score']
                down_points = play['away_score']
            else:
                lead_team = game_info['away_team']
                down_team = game_info['home_team']
                lead_points = play['away_score']
                down_points = play['home_score']
    
    if biggest_lead > biggest_lead_cutoff:
        rating = 0.6 + (biggest_lead/100.0)
        events.append(Event(rating, Event_Big_Lead(lead_team, down_team, lead_points, down_points, time_s)))
    
def calc_comeback():
    global events, game_info, game_plays, teams
    
    big_lead_cutoff = 18
    comeback_fail_cutoff = 4
    # means it was a back and forth, should do some other event,
    # not using right now
    other_team_lead_cutoff = 12
    
    home_biggest_lead = 0
    home_biggest_lead_qtr = 0
    away_biggest_lead = 0
    away_biggest_lead_qtr = 0
    for play in game_plays:
        cur_lead = play['home_score'] - play['away_score']
        if cur_lead > 0 and cur_lead > home_biggest_lead:
            home_biggest_lead = cur_lead
            home_biggest_lead_qtr = play['quarter']
        elif cur_lead < 0 and cur_lead > away_biggest_lead:
            away_biggest_lead = cur_lead
            away_biggest_lead_qtr = play['quarter']
    
    # TODO: check partial to show as win or not, also to include tie
    # home wins
    if away_biggest_lead > big_lead_cutoff:
        if cur_lead > 0: 
            rating = 0.5 + (away_biggest_lead_qtr*.1) + (cur_lead*.01)
            events.append(Event(rating, Event_Comeback(True, teams[game_info['home_team_id']], teams[game_info['away_team_id']], away_biggest_lead, away_biggest_lead_qtr, abs(cur_lead))))
        elif cur_lead < 0 and cur_lead >= -comeback_fail_cutoff:
            rating = 0.5 + (away_biggest_lead_qtr*.1) + (.2 / -cur_lead)
            events.append(Event(rating, Event_Comeback(False, teams[game_info['home_team_id']], teams[game_info['away_team_id']], away_biggest_lead, away_biggest_lead_qtr, abs(cur_lead))))
    if home_biggest_lead > big_lead_cutoff:
        if cur_lead < 0: 
            rating = 0.5 + (home_biggest_lead_qtr*.1) + (abs(cur_lead)*.01)
            events.append(Event(rating, Event_Comeback(True, teams[game_info['away_team_id']], teams[game_info['home_team_id']], home_biggest_lead, home_biggest_lead_qtr, abs(cur_lead))))
        elif cur_lead > 0 and cur_lead <= comeback_fail_cutoff:
            rating = 0.5 + (home_biggest_lead_qtr*.1) + (.2 / cur_lead)
            events.append(Event(rating, Event_Comeback(False, teams[game_info['away_team_id']], teams[game_info['home_team_id']], home_biggest_lead, home_biggest_lead_qtr, abs(cur_lead))))
    
"""
Event sorting and aggregating
These sort functions both sort the order of the events, and
aggregate certain specified events together. So a group of players with
similar stats could be grouped together as one event. Sorting and aggregating
functions can be added by calling the function in the sort_events function.
"""

def sort_team_high_stats():
    global events
    
    stat_rating_gap = 0.05
    
    new_events = []
    home_stat_groups = []
    away_stat_groups = []
    
    for event in events:
        if type(event.event) not in [Event_Stat]:
            new_events.append(event)
        else:
            if event.event.player.team == game_info['home_team']:
                if home_stat_groups and len(home_stat_groups[-1]) < 3 and home_stat_groups[-1][-1].rating < event.rating + stat_rating_gap:
                    home_stat_groups[-1].append(event)
                else:
                    home_stat_groups.append([event])
            else:
                if away_stat_groups and len(away_stat_groups[-1]) < 3 and away_stat_groups[-1][-1].rating < event.rating + stat_rating_gap:
                    away_stat_groups[-1].append(event)
                else:
                    away_stat_groups.append([event])
    
    #print([[(e.event.player.name, e.rating) for e in g] for g in home_stat_groups])
    #print([[(e.event.player.name, e.rating) for e in g] for g in away_stat_groups])
    
    stat_groups = home_stat_groups
    stat_groups.extend(away_stat_groups)
    
    for event_group in stat_groups:
        if len(event_group) == 1:
            new_events.append(event_group[0])
        else:
            rating = sum([e.rating for e in event_group]) / float(len(event_group))
            new_events.append(Event(rating, Event_Team_Rating([e.event.player for e in event_group])))
    events = new_events

def sort_sig_and_stat_events():
    global events, sig_events, stat_events
    
    sig_events = events[:3]
    for event in sig_events:
        if type(event.event) in [Event_Team_Rating, Event_Stat]:
            event.event.high = True
            event.event.calc_details()
    
    new_events = []
    for event in events[3:]:
        if type(event.event) in [Event_High_Overall_Stats, Event_Stat, Event_Team_Rating]:
            stat_events.append(event)
        else:
            new_events.append(event)
    events = sig_events + new_events
    
    stat_events = stat_events[:3]
    stat_events.sort(key = lambda k: (k.event.team, k.rating), reverse=True)
    if all([type(e.event) is Event_Team_Rating for e in stat_events]):
        stat_events = stat_events[:2]
        stat_events.sort(key = lambda k: (k.event.team, k.rating), reverse=True)

def calc_events():
    global events
    
    calc_high_stat_events()
    calc_high_overall_stats_events()
    calc_scoring_run()
    calc_last_second_shot()
    calc_big_lead()
    calc_comeback()
    
    sort_events()

def sort_events():
    global events
    
    events.sort(key = lambda k: k.rating, reverse=True)
    sort_team_high_stats()
    events.sort(key = lambda k: k.rating, reverse=True)
    sort_sig_and_stat_events()

def calc_sig_events():
    global sig_events
    
    sort_sig_events()
    
def sort_sig_events():
    sig_events.sort(key = lambda k: (k.rating), reverse=True)


"""
Game data calculations
These functions and Player class create the data structure to hold the current game state.
Statistics like player points, player fouls, and team records are calculated here.
"""

class Player:
    def __init__(self, foxsports_id, name, team):
        self.foxsports_id = foxsports_id
        self.name = name
        self.team = team
        self.points = 0
        self.assists = 0
        self.rebounds = 0
        self.offensive_rebounds = 0
        self.blocks = 0
        self.steals = 0
        self.turnovers = 0
        self.fouls = 0
        self.minutes = 0
        self.made_1 = 0
        self.made_2 = 0
        self.made_3 = 0
        self.missed_1 = 0
        self.missed_2 = 0
        self.missed_3 = 0
        self.points_1 = 0
        self.points_2 = 0
        self.points_3 = 0
        self.points_4 = 0
        self.points_5 = 0
        self.db = nba_db.get_player_foxsports(foxsports_id)
        if self.name is None:
            self.name = str(self.db.first_name) + " " + str(self.db.last_name)

    def __repr__(self):
        return str(self.get_dict())
    
    def get_dict(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        d = dict([a for a in attributes if not(a[0] == "db") and not(a[0].startswith('__') and a[0].endswith('__'))])
        if self.db:
            d.update(self.db.get_dict())
        return d


def calc_shot(play):
    global players
    add_player(play['p_player_id'], play['primary_player'], play['name'], play)
    if play['points_worth'] and play['shot_made'] == 'makes':
        players[play['p_player_id']].points += int(play['points_worth'])
        add_quarter_points(play['p_player_id'], int(play['quarter']), int(play['points_worth']))
        
def calc_assist(play):
    global players
    add_player(play['s_player_id'], play['secondary_player'], play['name'], play)
    if play['points_worth'] and play['shot_made'] == 'makes':
        players[play['s_player_id']].assists += 1
    calc_shot(play)
     
def calc_freethrow(play):
    calc_shot(play)

def calc_rebound(play):
    global players
    if play['p_player_id']:
        add_player(play['p_player_id'], play['primary_player'], play['name'], play)
        players[play['p_player_id']].rebounds += 1

# a technical foul can have no p_player_id
def calc_foul(play):
    global players, events

    if not play['p_player_id']:
        return
    add_player(play['p_player_id'], play['primary_player'], play['name'], play)
    players[play['p_player_id']].fouls += 1
    
    if players[play['p_player_id']].fouls == 6:
        rating = 0.5 + (0.4 / int(play['quarter']))
        time_left = (int(play['quarter']), int(play['minutes']), int(play['seconds']))
        events.append(Event(rating, Event_Foul_Out(players[play['p_player_id']], time_left)))

# Needs to be implemented differently for FoxSports
def calc_steal(play):
    global players
    add_player(play['p_player_id'], play['primary_player'], play['name'])
    add_player(play['s_player_id'], play['secondary_player'], play['name'])
    players[play['p_player_id']].steals += 1
    players[play['s_player_id']].turnovers += 1

def calc_block(play):
    global players
    add_player(play['p_player_id'], play['primary_player'], play['name'], play)
    players[play['p_player_id']].blocks += 1
    
def add_quarter_points(p_player_id, quarter, points):
    global players
    if quarter == 1:
        players[p_player_id].points_1 += points
    elif quarter == 2:
        players[p_player_id].points_2 += points
    elif quarter == 3:
        players[p_player_id].points_3 += points
    elif quarter == 4:
        players[p_player_id].points_4 += points
    else:
        players[p_player_id].points_5 += points
    

# changed to include current game results
def calc_record():
    global game_info, partial
    
    game_id = game_info['game_id'] if not partial else int(game_info['game_id']) - 1
    
    conn = sqlite3.connect(dg.db_filepath)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("SELECT case when (home_team_score > away_team_score and team.id = home_team_id) or (away_team_score > home_team_score and team.id = away_team_id) then 'W' else 'L' end as WL from team, schedule "
                   "where team.id = " + str(game_info['home_team_id']) + " "
                   "and (home_team_id = team.id or away_team_id = team.id) "
                   "and game_id <= " + str(game_id) + " "
                   "order by game_id desc")
    record_data = cursor.fetchall()
    if not record_data:
        record_data = []
    
    wins = 0
    losses = 0
    
    for game in record_data:
        if game['WL'] == 'W':
            wins += 1
        else:
            losses += 1
    game_info['home_wins'] = wins
    game_info['home_losses'] = losses
    
    cursor.execute("SELECT case when (home_team_score > away_team_score and team.id = home_team_id) or (away_team_score > home_team_score and team.id = away_team_id) then 'W' else 'L' end as WL from team, schedule "
                   "where team.id = " + str(game_info['away_team_id']) + " "
                   "and (home_team_id = team.id or away_team_id = team.id) "
                   "and game_id <= " + str(game_id) + " "
                   "order by game_id desc")
    record_data = cursor.fetchall()
    if not record_data:
        record_data = []
    
    wins = 0
    losses = 0
    
    for game in record_data:
        if game['WL'] == 'W':
            wins += 1
        else:
            losses += 1
    game_info['away_wins'] = wins
    game_info['away_losses'] = losses

# NOTE: Some rebounds have no player or player_id attached to them
#       will just live with
def add_player(player_id, player_name, team_name, t_index=0):
    global players
    if player_id and player_name and player_id not in list(players.keys()):
        players[player_id] = Player(player_id, player_name, team_name)
        players[player_id].db = nba_db.get_player_foxsports(player_id)

"""
calculate_stats
Data for the current game state is calculated in this function.
The player stats is calculated by iterating through the play-by-plays and incrementing stats
there when neccessary.
"""

def calculate_stats():
    global game_plays
    
    calc_record()
    
    for play_index, play in enumerate(game_plays):        
        if play['play_type'] == "shot":
            calc_shot(play)
        elif play['play_type'] == "assist":
            calc_assist(play)
        elif play['play_type'] == "blocks":
            calc_block(play)
        elif play['event_description'] == "Foul":
            calc_foul(play)
        elif play['play_type'] == "rebound":
            calc_rebound(play)
        elif play['play_type'] == "steal":
            #calc_steal(play)
            pass
        elif play['play_type'] == "substitution":
            pass
        elif play['play_type'] == "timeout":
            pass
        elif play['play_type'] == "jump ball":
            pass
        elif play['play_type'] == "free throw":
            calc_freethrow(play)
        elif DEBUG:
            pass

# Returns a string for the given quarter.
# Ex. 3 -> the 3rd quarter, 6 -> double overtime
def get_quarter_str(quarter):
    quarter_str = ""
    if quarter <= 4:
        quarter_str = "the " + num_ordinal(quarter) + " quarter"
    elif quarter == 6:
        quarter_str = "double overtime"
    elif quarter == 7:
        quarter_str = "triple overtime"
    else:
        quarter_str = "overtime"
    return quarter_str

# Adds any extra data to the game_info global variable
def game_info_passthrough():
    global game_info
    game_info['teams'] = [game_info['home_team'], game_info['away_team']]

# Adds any extra data to the game_plays global list variable
def game_plays_passthrough():
    global game_plays
    for play_index, play in enumerate(game_plays):
        # add play index number
        play['play_index'] = play_index
        
        # add points worth string
        if play['points_worth']:
            play['points_worth_str'] = "one" if play['points_worth'] == 1 else "two" if play['points_worth'] == 2 else "three"
            
        # add quarter string
        if play['quarter']:
            play['quarter_str'] = num_ordinal(play['quarter'])
    

"""
Central location for outputting text
out_type 0 is for debug. Prints to console.
out_type 1 is for HTML output. Constructs an HTML web page article.
"""
def parse_recap_strings(output_strings, out_type=0, web_type=0):
    if out_type == 0:
        if output_strings:
            print(' '.join(output_strings))
    elif out_type == 1:
        print_to_web(output_strings, web_type)

"""
HTML document constructing functions
"""
def print_to_web(output, web_type=0):
    file_name = web_dir + str(game_info['game_code']) + ".html"
    
    if web_type == 0:
        if not os.path.exists(web_dir):
            os.makedirs(web_dir)
            
        f = open(file_name, "w")
    else:
        f = open(file_name, "a")
    
    if (web_type == 0):
        f.write(web_get_header(output))
    elif (web_type == 1):
        f.write(web_get_short_summaries(output))
    elif (web_type == 2):
        f.write(web_get_long_summaries(output))
    elif (web_type == 3):
        f.write(web_get_record(output))
    elif (web_type == 4):
        f.write(web_get_stats(output))
    elif (web_type == 5):
        f.write(web_get_significant_events(output))
    elif (web_type == 6):
        f.write(web_get_link(output))
    elif (web_type == 7):
        f.write(web_close())
    
    f.close()
    
def web_get_header(output):
    title = output[0].rstrip('.')
    
    header = """<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8"> 
    <title>"""
    header += title
    header += """</title>
    <link rel="stylesheet" type="text/css" href="../css/style.css">
</head>

<body>
    <h1>"""
    header += title
    header += """</h1>
    </br>
    <h2 style="color:gray">by NBANLP Recap Generator</h2>
    
    </br></br>\n"""
    
    return header

def web_get_short_summaries(story_list):
    #summary = "\t<h3>Summary</h3>\n"
    summary = ""
    
    summary += web_get_image()
    
    if story_list:
        summary += "\t<p>"
        summary += " ".join(story_list)
        summary += "</p>"
    #summary += "\n\n\t</br>\n"
    summary += "\n\n\n"
    
    return summary

# Gets a general emotion-neutral image of the home team.
def web_get_image():
    global game_info
    
    img_dir = "./web/img/"
    home_team = "%02d" % game_info["home_team_id"]
    team_dir = img_dir + home_team + "/"
    img_list = glob.glob(os.path.join(team_dir, '*.jpg'))
    img_index = random.randrange(len(img_list)) + 1
    img_path = "../img/" + home_team + "/%02d" % img_index + ".jpg"
    
    string = '\t<img src="' + img_path
    string += '" alt="No image loaded" align="right" style="height:50%; width:50%;margin-left:20px;margin-bottom:20px;">\n'
    return string

def web_get_long_summaries(story_list):
    summary = "\t<h3>Stories</h3>\n"
    summary = ""
    
    for story in story_list:
        summary += "\t<p>"
        summary += " ".join(story)
        summary += "</p>\n\n"
    #summary += "\t</br>\n"
    summary += "\n"
    
    return summary

def web_get_record(output):
    summary = "\t<h3>Record</h3>\n"
    summary = ""
    
    if output:
        summary += "\t<p>"
        summary += " ".join(output)
        summary += "</p>"
    #summary += "\n\n\t</br>\n"
    summary += "\n\n\n"
    
    return summary

def web_get_stats(stats_list):
    summary = "\t<h3>Stats</h3>\n"
    summary = ""
    
    if stats_list:
        summary += "\t<p>"
        summary += "\n\t".join([stat for stat in map(lambda k: " ".join(k), stats_list) if stat])
        summary += "</p>"
    #summary += "\n\n\t</br>\n"
    summary += "\n\n\n"
    
    return summary

def web_get_significant_events(story_list):
    summary = "\t<h3>Significant Events</h3>\n"
    summary = ""
    
    for story in story_list:
        summary += "\t<p>"
        summary += " ".join(story)
        summary += "</p>\n\n"
    #summary += "\t</br></br>\n"
    summary += "\n"
    
    return summary

def web_get_link(output_link):
    summary = "\t<h3>NBC recap url for reference</h3>\n"
    
    if output_link:
        summary += "\t<a href=" + str(output_link) + ' target="_blank">'
        summary += str(output_link) + '</a>'
    #summary += "\n\n\t</br>\n"
    summary += "\n\n\n"
    
    return summary

def web_close():
    closing = "\n\n\n</body>\n\n</html>\n"

    return closing

"""
Used to choose a random recap template string from a list in recap_strings.
The chosen template string is filled with the variables in info.
"""
def recap_string_from_list(strings, info):
    i = random.randint(0, len(strings) - 1)
    return strings[i][0] % tuple(info[key] for key in strings[i][1])

# Used to debug print game plays to console
def parse_comment(play, game_time):
    time_string = "Q" + str(game_time[0]) + " " + str(game_time[1]) + ':%02d' % (game_time[2],)
    time_string +=  " " + str(game_info['home_team']) + " " + str(game_time[3]) + "-" + str(game_time[4]) + " " + str(game_info['away_team'])
    
    print(time_string)
    print(play['play_type'],":",play['description'])
    print(play)
    print()

# Gets a Player list for the given team
def get_players(team_id, team):
    players = nba_db.get_team(team_id)
    player_list = []
    for p in players:
        new_p = Player(p.foxsports_id, p.first_name + " " + p.last_name, team.name)
        new_p.db = p
        player_list.append(new_p)
    players_dict = dict([(p.foxsports_id, p) for p in player_list])
    return players_dict

# Gets a dict of nba_db Team objects for the given teams.
def get_teams(home_team_id, away_team_id):
    home_team = nba_db.get_team_data(home_team_id)
    away_team = nba_db.get_team_data(away_team_id)
    return dict([(home_team_id, home_team), (away_team_id, away_team)])

# Retrieves the game_info for the current game. This includes teams, scores, cities, and other info
def get_game_info(game_id):
    conn = sqlite3.connect(dg.db_filepath)
    conn.row_factory = dict_factory

    headers = ['season', 'game_date', 'home_team', 'away_team', 'game_type', 'home_score', 'away_score', 'game_code', 'stadium']
    
    
    cursor = conn.cursor();
    cursor.execute("SELECT season, game_date, t1.name as home_team, t1.city as home_city, t2.name as away_team, t2.city as away_city, game_type, home_score, away_score, game_code, stadium, home_team as home_team_id, away_team as away_team_id "
                   "FROM game JOIN team as t1 "
                   " ON home_team = t1.id JOIN team as t2 "
                   " ON away_team = t2.id "
                   "WHERE game.id = " + str(game_id))
    game_info = cursor.fetchone()
    
    if not game_info:
        return None
    
    cursor.execute("SELECT home_team_score, away_team_score "
                   "FROM schedule "
                   "WHERE game_id = " + str(game_id))
    game_info.update(cursor.fetchone())
    
    # get winner / loser
    if game_info['home_team_score'] > game_info['away_team_score']:
        game_info['winner_team_name'] = game_info['home_team']
        game_info['winner_score'] = game_info['home_team_score']
        game_info['winner_city'] = game_info['home_city']
        game_info['loser_team_name'] = game_info['away_team']
        game_info['loser_score'] = game_info['away_team_score']
        game_info['loser_city'] = game_info['away_city']
    else:
        game_info['winner_team_name'] = game_info['away_team']
        game_info['winner_score'] = game_info['away_team_score']
        game_info['winner_city'] = game_info['away_city']
        game_info['loser_team_name'] = game_info['home_team']
        game_info['loser_score'] = game_info['home_team_score']
        game_info['loser_city'] = game_info['home_city']
    game_info['lead'] = int(game_info['winner_score']) - int(game_info['loser_score'])
    
    game_info['game_id'] = game_id
    return game_info

# Retrieves the list of play_by_plays for the given game.
# If a partial game is chosen, only those plays before the given cutoff partial_time are retrieved.
def get_game_plays(game_id):
    global partial, partial_time
    
    conn = sqlite3.connect(dg.db_filepath)
    conn.row_factory = dict_factory
    
    plays = []
    headers = ['play_by_play.id as pbp_id', 'event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type', 'points_worth', 'p_player_id', 's_player_id']
    
    cursor = conn.cursor()
    if partial:
        cursor.execute("SELECT " + ','.join(headers) + ", name, team.id as t_id FROM play_by_play JOIN team ON team.id = play_by_play.team_id where game_id = " + str(game_id) + " " +
                       "AND (quarter < ?" + 
                       " OR quarter == ? AND minutes > ?" +
                       " OR quarter == ? AND minutes == ? AND seconds >= ?)", (partial_time[0], partial_time[0], partial_time[1], partial_time[0], partial_time[1], partial_time[2]))
    else:
        cursor.execute("SELECT " + ','.join(headers) + ", name, team.id as t_id FROM play_by_play JOIN team ON team.id = play_by_play.team_id where game_id = ?", [game_id])
    data = cursor.fetchall()
    
    return data

# Adds any extra data if the current game is a partial game.
def partial_passthrough():
    global game_plays, game_info, partial_time
    last_play = game_plays[-1]
    
    game_info['quarter_str'] = num_ordinal(partial_time[0])
    game_info['quarter'] = partial_time[0]
    game_info['minutes'] = partial_time[1]
    game_info['seconds'] = partial_time[2]
    
    game_info['home_team_score'] = game_info['home_score'] = last_play['home_score']
    game_info['away_team_score'] = game_info['away_score'] = last_play['away_score']
    if game_info['home_team_score'] > game_info['away_team_score']:
        game_info['winner_team_name'] = game_info['home_team']
        game_info['winner_score'] = game_info['home_team_score']
        game_info['winner_city'] = game_info['home_city']
        game_info['loser_team_name'] = game_info['away_team']
        game_info['loser_score'] = game_info['away_team_score']
        game_info['loser_city'] = game_info['away_city']
    else:
        game_info['winner_team_name'] = game_info['away_team']
        game_info['winner_score'] = game_info['away_team_score']
        game_info['winner_city'] = game_info['away_city']
        game_info['loser_team_name'] = game_info['home_team']
        game_info['loser_score'] = game_info['home_team_score']
        game_info['loser_city'] = game_info['home_city']
    game_info['lead'] = int(game_info['winner_score']) - int(game_info['loser_score'])

"""
interface_main
This is the main function to interface with the user.
Options are givent to the user to do the following:
1) 1 - max_num: generate a selection available articles
2) ALL: generate all available articles
3) PARTIAL: generate partial game recap articles
4) IMPORT: import downloaded scraped data into the NBA Database
5) SCRAPE: scrape game and schedule data from the web to the local machine
"""
def interface_main():
    global DEBUG
    
    if len(sys.argv) > 1:
        DEBUG = 'debug' in sys.argv
            
    # Look for data
    num_games = interface_check_games()
    if num_games > 0:
        game_nums = input("Enter games between 1 and " + str(num_games) + ", or ALL, or PARTIAL, or IMPORT, or SCRAPE: ")
        if "IMPORT" in str.upper(game_nums):
            interface_import_games(importting=True)
            interface_scrape_game_schedules(importting=True)
            return
        if "SCRAPE" in str.upper(game_nums):
            interface_scrape_game_schedules(scraping=True)
            interface_scrape_games(scraping=True)
            return
        if "PARTIAL" in str.upper(game_nums):
            qms_str = input("Enter [quarter minutes seconds]: ")
            partial_time = tuple(map(int, qms_str.split()))
            partial = True
            game_nums = input("Enter games between 1 and " + str(num_games) + ", or ALL: ")
        else:
            partial = False
            partial_time=(4,0,0)
        if "ALL" in str.upper(game_nums):
            game_nums = list(range(1, (num_games + 1)))
        else:
            game_nums = list(map(int, game_nums.split()))
        try:
            print("Generating Articles. Press ctrl-c to end early.")
            for game_id in game_nums:
                try:
                    file_name = gen_article(game_id, partial, partial_time, debug=DEBUG)    
                    print("Game", game_id, "written to", file_name)
                except KeyboardInterrupt:
                    print("Article generation ended early by user.", game_id, "removed or not written.")
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    break
                except:
                    print("Error: Game", game_id)
        except KeyboardInterrupt:
            print("Article generation ended early by user. Game", game_id, "removed or not written.")
            if os.path.exists(file_name):
                os.remove(file_name)
            
    else:
        print("Please import some data.")
    

def interface_check_games():
    if not nba_db.is_db_exists():
        print("NBA Database not found in", dg.db_filepath)
        create_db(dg.data_path)
    
    num_games = nba_db.get_db_game_count()
    if num_games <= 0:
        print("No games found. Preparing to import...")
        interface_import_games()
        old_num_games = num_games
        num_games = nba_db.get_db_game_count()
        print("Imported", str(num_games - old_num_games), "new games into NBA Database.")
    
    return num_games
        
def interface_import_games(importting=False):
    num_games = nba_scrapers.get_scraper_dir_count(sg.scraper_path)
    
    if num_games <= 0 and not importting:
        print(str(num_games), "games found in", sg.cur_gamedata_path + ". Preparing to scrape for game data...")
        interface_scrape_games()
        old_games = num_games
        num_games = nba_scrapers.get_scraper_dir_count(sg.scraper_path)
        print("Scraped", str(num_games - old_games), "games into", sg.cur_gamedata_path + ".")
        
    response = input(str(num_games) + " games found in " + sg.cur_gamedata_path + ". Import games?[y/n]: ")
    if response == "y":
        nba_scrapers.import_dir_into_db(sg.cur_gamedata_path)

def interface_scrape_games(scraping=False):
    num_games = nba_db.get_db_schedule_count()
    
    if num_games <= 0 and not scraping:
        print(str(num_games), "scheduled games found in NBA Database. Preparing to import game schedules...")
        interface_scrape_game_schedules()
        old_games = num_games
        num_games = nba_db.get_db_schedule_count()
        #num_games = nba_scrapers.get_scraper_dir_count()
        print("imported", str(num_games - old_games), "game schedules into", sg.cur_gameschedule_path + ".")
        
    response = input(str(num_games) + " scheduled games found in NBA Database. Scrape game data?[y/n]: ")
    old_games = nba_scrapers.get_scraper_dir_count(sg.scraper_path)
    if response == "y":
        # Scrape for game data using shedules table
        nba_scrapers.scrape_games(sg.scraper_path)
    if scraping:
        num_games = nba_scrapers.get_scraper_dir_count(sg.scraper_path)
        print("Scraped", str(num_games - old_games), "games into", sg.cur_gamedata_path + ".")

def interface_scrape_game_schedules(importting=False, scraping=False):
    num_games = nba_scrapers.get_scraper_schedule_dir_count(sg.scraper_path)
    
    if num_games <= 0 and not importting or scraping:
        if num_games <= 0:
            print(str(num_games), "game schedules found in", sg.cur_gameschedule_path + ". Preparing to scrape for game schedules...")
        if not importting:
            response = input("Scrape foxsports season 2014-2015 for schedule data?[y/n]")
            if response == "y":
                # scrape game schedule jsons from web into folder
                nba_scrapers.scrape_game_schedules(sg.scraper_path)
        old_games = num_games
        num_games = nba_scrapers.get_scraper_schedule_dir_count(sg.scraper_path)
        print("Scraped", str(num_games - old_games), "game schedules into", sg.cur_gameschedule_path + ".")
    
    if not scraping:
        response = input(str(num_games) + " games schedules found in " + sg.cur_gameschedule_path + ". Import?[y/n]: ")
        if response == "y":
            # import game schedule jsons into schedule table
            nba_scrapers.import_schedule_dir_into_db(sg.scraper_path)

"""
gen_article
This is the main function to generate an article.
An article is generated from the game specified by game_id with the matching NBA Database game of the game_id.
1) Game data is retrieved
2) Game stats are calculated
3) Events are discovered and sorted
3) 
"""
def gen_article(game_id, partial_var=False, partial_time_var=(4,0,0), debug=DEBUG):
    global DEBUG, game_info, game_plays, teams, players, events, sig_events, stat_events, partial, partial_time
    
    DEBUG = debug
    partial = partial_var
    partial_time = partial_time_var
    print_to_web = not DEBUG
    output_dest = 1 if print_to_web else 0
    
    game_info = get_game_info(game_id)
    game_plays = get_game_plays(game_id)
    
    if not game_info:
        print('game_id',game_id,'not found')
        return

    teams = get_teams(game_info['home_team_id'], game_info['away_team_id'])
    players = get_players(game_info['home_team_id'], teams[game_info['home_team_id']])
    players.update(get_players(game_info['away_team_id'], teams[game_info['away_team_id']]))
    game_info_passthrough()
    game_plays_passthrough()
    if partial:
        partial_passthrough()
    
    """
    print out game plays if in debug
    """

    if DEBUG:
        print('game_id:', game_id)
        print(game_info)
        
        for play_index, play in enumerate(game_plays):
            game_time = (play['quarter'], play['minutes'], play['seconds'], play['home_score'], play['away_score'], play_index)
            
            if play['play_type'] in ['shot', 'assist', 'blocks']:
                parse_comment(play, game_time)
            elif play['event_description'] == "Foul":
                parse_comment(play, game_time)
            elif play['play_type'] == "rebound":
                parse_comment(play, game_time)
            elif play['play_type'] == "steal":
                parse_comment(play, game_time)
            elif play['play_type'] == "substitution":
                parse_comment(play, game_time)
            elif play['play_type'] == "timeout":
                parse_comment(play, game_time)
            elif play['play_type'] == "jump ball":
                parse_comment(play, game_time)
            elif play['play_type'] == "free throw":
                parse_comment(play, game_time)
            elif DEBUG:
                print("UNPARSED PLAY_TYPE:", play['play_type'], "\n")
        
        print("NBC recap url:")
        print("http://scores.nbcsports.msnbc.com/nba/recap.asp?g=" + str(game_info['game_code']) + '\n')
    
    """
    Recaps
    """
    events = []
    sig_events = []
    stat_events = []
    
    # Gets stats
    calculate_stats()
    if DEBUG:
        for player in players.values():
            print("\n" + str(player.name) + " " + str(player))
    calc_events()
    if DEBUG:
        print(events)
    
    # Headline
    if output_dest == 0:
        print("HEADLINE")
    parse_recap_strings(gen_headline(game_info), output_dest, 0)
    
    # Intro
    # probably won't use at all anymore
    #print("\nINTRO")
    
    # Summary
    # Change to include all top story descriptive paragraphs
    if output_dest == 0:
        print("\nSHORT SUMMARY STORIES")
    parse_recap_strings([event.gen_summary() for event in sig_events], output_dest, 1)
    
    # Stories
    if output_dest == 1:
        parse_recap_strings([event.gen_story() for event in events], output_dest, 2)
    else:
        print("\nLONG SUMMARY STORIES")
        for event in events:
            print("r:", str(event.rating))
            parse_recap_strings(event.gen_story())
            print()
    
    # Record and standings
    if output_dest == 0:
        print("\nRECORD")
    parse_recap_strings(gen_record(game_info), output_dest, 3)
    
    # Stat summary
    sorted_players = sorted(players.values(), key=lambda k : (k.team, -k.points, -k.assists, str(k.name)))
    if output_dest == 1:
        #parse_recap_strings([gen_stat(player.get_dict()) for player in sorted_players], output_dest, 4)
        parse_recap_strings([event.gen_story() for event in stat_events], output_dest, 4)
    elif output_dest == 0:
        print("\nSTATS")
        for event in stat_events:
            print("r:", str(event.rating))
            parse_recap_strings(event.gen_story())
            print()
        #for player in sorted_players:
        #    parse_recap_strings(gen_stat(player.get_dict()))
    
    # Significant events
    # if output_dest == 0:
    #     print("\nSIGNIFICANT EVENTS")
    #     for event in [["..."]]:
    #         parse_recap_strings(event)
    #         print()
    # elif output_dest == 1:
    #     parse_recap_strings([["..."]], output_dest, 5)
    
    # URL for reference
    if DEBUG:
        reference_link = "http://scores.nbcsports.msnbc.com/nba/recap.asp?g=" + str(game_info['game_code'])
        if output_dest == 0:
            print("\n\n\n\nNBC recap url for reference:")
            print(reference_link + '\n\n\n\n')
        elif output_dest == 1:
            parse_recap_strings(reference_link, output_dest, 6)
    
    parse_recap_strings(None, output_dest, 7)
    
    file_name = web_dir + str(game_info['game_code']) + ".html"
    return file_name
    
    
if __name__ == '__main__':
    #main()
    interface_main()
