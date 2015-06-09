# NBA NLP - Senior Project - Spring 2015
# NBA Database - Main Interface
# Jacob Bustamante

"""
nba_db
This is the main interfacing class for working with NBA Database, the sqlite db file.
The classes Game, Team, and Player are used as input to load into the db and output when retrieving from the db.
These functions are used to retrieve the desired data or insert into db.
"""

import sqlite3
import os, inspect
import data.data_globals as dg

db_filename = dg.db_filepath

class Game:
    def __init__(self, d=None, season=None, game_date=None, home_team=None, away_team=None, game_type=None, home_score=None, away_score=None, stadium=None, game_code=None):
        if d:
            self.season = d['season']
            self.game_date = d['game_date']
            self.home_team = d['home_team']
            self.away_team = d['away_team']
            self.game_type = d['game_type']
            self.home_score = d['home_score']
            self.away_score = d['away_score']
            self.stadium = d['stadium']
            self.game_code = d['game_code']
        else:
            self.season = season
            self.game_date = game_date
            self.home_team = home_team
            self.away_team = away_team
            self.game_type = game_type
            self.home_score = home_score
            self.away_score = away_score
            self.stadium = stadium
            self.game_code = game_code

    def __repr__(self):
        return str(self.get_dict())
    
    def get_dict(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        d = dict([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])
        return d

class Team:
    def __init__(self, d=None, team_id=None, city=None, alias=None, name=None, division=None):
        if d:
            self.id = d['id']
            self.team_id = d['id']
            self.city = d['city']
            self.alias = d['alias']
            self.name = d['name']
            self.division = d['division']
        else:
            self.id = team_id
            self.team_id = team_id
            self.city = city
            self.alias = alias
            self.name = name
            self.division = division

    def __repr__(self):
        return str(self.get_dict())
    
    def get_dict(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        d = dict([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])
        return d


class Player:
    def __init__(self, d=None, team_id=None, first_name=None, last_name=None, weight=None, height=None, jersey_number=None, experience=None, age=None, first_year=None, school=None, primary_position=None, secondary_position=None, foxsports_id=None):
        if d:
            self.first_name = d['first_name']
            self.last_name = d['last_name']
            self.weight = d['weight']
            self.height = d['height']
            self.jersey_number = d['jersey_number']
            self.experience = d['experience']
            self.age = d['age']
            self.first_year = d['first_year']
            self.school = d['school']
            self.primary_position = d['primary_position']
            self.secondary_position = d['secondary_position']
            self.foxsports_id = d['foxsports_id']
            self.team_id = d['team_id']
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.weight = weight
            self.height = height
            self.jersey_number = jersey_number
            self.experience = experience
            self.age = age
            self.first_year = first_year
            self.school = school
            self.primary_position = primary_position
            self.secondary_position = secondary_position
            self.foxsports_id = foxsports_id
            self.team_id = team_id

    def __repr__(self):
        return str(self.get_dict())
    
    def get_dict(self):
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        d = dict([a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])
        return d


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_set_update_string(d):
    keys = [key for key in d.keys() if d[key] not in [None,"None", ""]]
    cols = ",".join([(key + "=?") for key in keys])
    vals = [d[key] for key in keys]
    return (cols, vals)

def get_insert_string(d):
    keys = [key for key in d.keys() if d[key] not in [None,"None", ""]]
    cols = ",".join(keys)
    q = ','.join(['?'] * len(keys))
    vals = [d[key] for key in keys]
    return (cols, q, vals)

def is_db_exists():
    return os.path.exists(db_filename)

def get_db_game_count():
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor();
        cursor.execute("SELECT count(*) as count "
                       "FROM game ")
        info = cursor.fetchone()
        
        return info['count']

def get_db_schedule_count():
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor();
        cursor.execute("SELECT count(*) as count "
                       "FROM schedule ")
        info = cursor.fetchone()
        
        return info['count']

def get_scheduled_games():
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor();
        cursor.execute("SELECT game_date, home_team_id, away_team_id "
                       "FROM schedule ")
        games = cursor.fetchall()
        
        return games

def get_game_code(game_id):
    game_info = {}
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor();
        cursor.execute("SELECT game_code "
                       "FROM game "
                       "WHERE game.id = " + str(game_id))
        game_info = cursor.fetchone()
    
    if game_info:
        return game_info['game_code']
    else:
        return None

def get_team_data(team_id):
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, city, alias, name, division "
                       "FROM team "
                       "WHERE team.id = ?", [team_id])
        team = cursor.fetchone()
    return Team(team)

def get_player_foxsports(foxsports_id):
    with sqlite3.connect(db_filename) as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT id, team_id, first_name, last_name, weight, height, jersey_number, experience, age, first_year, school, primary_position, secondary_position, foxsports_id "
                           "FROM player "
                           "WHERE player.foxsports_id = ?", [foxsports_id])
            player = cursor.fetchone()
    return Player(d=player)

def get_team(team_id):
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT id, team_id, first_name, last_name, weight, height, jersey_number, experience, age, first_year, school, primary_position, secondary_position, foxsports_id "
                       "FROM player "
                       "WHERE player.team_id = ?", [team_id])
        players = cursor.fetchall()
    return [Player(d=p) for p in players]

# can possibly replace with an insert or update call
def insert_player_foxsports(player):
    foxsports_id = player.foxsports_id
    team_id = player.team_id
    if not foxsports_id or not team_id:
        print("ERROR: insert_player_foxsports, foxsports_id or team_id missing:", player)
        return
    
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT 0 "
                       "FROM player "
                       "WHERE player.foxsports_id = ?", [foxsports_id])
        found = cursor.fetchone()
        if found:
            cols, vals = get_set_update_string(player.get_dict())
            vals.extend([foxsports_id, team_id])
            cursor.execute("UPDATE player "
                       "SET " + cols + " "
                       "WHERE player.foxsports_id = ? "
                       "AND player.team_id = ? ", vals)
        else:
            cols, flags, vals = get_insert_string(player.get_dict())
            cursor.execute("INSERT INTO player "
                       "( " + cols + ") "
                       "VALUES (" + flags + ")", vals)

def insert_game_foxsports(game):
    foxsports_id = game.game_code
    if not foxsports_id:
        print("ERROR: insert_game_foxsports, game_code missing:", game)
        return
    
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT 0 "
                       "FROM game "
                       "WHERE game.game_code = ?", [foxsports_id])
        found = cursor.fetchone()
        if found:
            cols, vals = get_set_update_string(game.get_dict())
            vals.extend([foxsports_id])
            cursor.execute("UPDATE game "
                       "SET " + cols + " "
                       "WHERE game.game_code = ? ", vals)
        else:
            cols, flags, vals = get_insert_string(player.get_dict())
            cursor.execute("INSERT INTO game "
                       "( " + cols + ") "
                       "VALUES (" + flags + ")", vals)

def get_team_streak(team_id, cur_game_id):
    return get_team_last_few(team_id, cur_game_id, streak=True)

# returns (num_games, wins, losses)
def get_team_last_few(team_id, cur_game_id, streak=False, games_back=10):
    with sqlite3.connect(db_filename) as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT case when (home_team_score > away_team_score and team.id = home_team_id) or (away_team_score > home_team_score and team.id = away_team_id) then 'W' else 'L' end as WL from team, schedule "
                       "where team.id = ? "
                       "and (home_team_id = team.id or away_team_id = team.id) "
                       "and game_id <= ? "
                       "order by game_id desc", [team_id, cur_game_id])
        prev_games = cursor.fetchall()
        if not prev_games:
            return(0, 0, 0)
        
        #(wins, losses)
        wins = 0
        losses = 0
        prev_games_ratio = []
        if not streak:
            prev_games = prev_games[:games_back]
        for game in prev_games:
            if game['WL'] == 'W':
                wins += 1
            else:
                losses += 1
            prev_games_ratio.append((wins, losses))
    
        if streak:
            win_per = [(w, l) for (w, l) in prev_games_ratio if w/(w+l) >= 1.0 and w >= 2]
            loss_per = [(l, w) for (w, l) in prev_games_ratio if l/(w+l) >= 1.0 and l >= 2]
        else:
            win_per = [(w, l) for (w, l) in prev_games_ratio if w/(w+l) >= .8 and w >= 3]
            loss_per = [(l, w) for (w, l) in prev_games_ratio if l/(w+l) >= .8 and l >= 3]
    
        if win_per:
            max_win = max(win_per)
            num_past_games = max_win[0] + max_win[1]
            num_won = max_win[0]
            num_loss = max_win[1]
            return(num_past_games, num_won, num_loss)
        elif loss_per:
            max_loss = max(loss_per)
            num_past_games = max_loss[0] + max_loss[1]
            num_won = max_loss[1]
            num_loss = max_loss[0]
            return(num_past_games, num_won, num_loss)
        else:
            return(0,0,0)

