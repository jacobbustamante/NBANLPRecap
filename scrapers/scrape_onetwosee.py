# NBA NLP - Senior Project - Spring 2015
# Scrapers - onetwosee
# Jacob Bustamante

import os, sys, time, re, json, urllib
from glob import glob
from bs4 import BeautifulSoup
from data import nba_db
import scrapers.insert_into_db as insert_into_db

teams = {
    'Atlanta Hawks' : '01',
    'Boston Celtics' : '02',
    'New Orleans Pelicans' : '03',
    'Chicago Bulls' : '04',
    'Cleveland Cavaliers' : '05',
    'Dallas Mavericks' : '06',
    'Denver Nuggets' : '07',
    'Detroit Pistons' : '08',
    'Golden State Warriors' : '09',
    'Houston Rockets' : '10',
    'Indiana Pacers' : '11',
    'Los Angeles Clippers' : '12',
    'Los Angeles Lakers' : '13',
    'Miami Heat' : '14',
    'Milwaukee Bucks' : '15',
    'Minnesota Timberwolves' : '16',
    'Brooklyn Nets' : '17',
    'New York Knicks' : '18',
    'Orlando Magic' : '19',
    'Philadelphia 76ers' : '20',
    'Phoenix Suns' : '21',
    'Portland Trail Blazers' : '22',
    'Sacramento Kings' : '23',
    'San Antonio Spurs' : '24',
    'Oklahoma City Thunder' : '25',
    'Utah Jazz' : '26',
    'Washington Wizards' : '27',
    'Toronto Raptors' : '28',
    'Memphis Grizzlies' : '29',
    'Charlotte Hornets' : '30'
    #'Charlotte Bobcats' : '30'
}
team_id_name = dict([(int(teams[t]), t) for t in teams.keys()])

def extract_json_from_foxsports():
    games_dir = './webpages/foxsports_gamepages_2015/'
    onetwosee_dir = "./webpages/onetwosee_2015/"
    
    for html_file in os.listdir(games_dir):
        if ".html" in html_file[-5:]:
            with open(games_dir + html_file) as open_file:
                soup = BeautifulSoup(open_file)
                script = soup.find('script', text=re.compile('nba\.initialUpdate'))
                json_data = re.search(r'nba\.initialUpdate\s*=\s*({.*?})\s*;', script.string).group(1)
                with open(onetwosee_dir + html_file[:-5] + ".json", "w") as open_file:
                    open_file.write(json_data)

def parse_game_info(data):
    season = data['gameInfo']['season']['season']
    game_date = data['gameInfo']['date']
    home_team = data['gameInfo']['home-team']['team-code']['id']
    away_team = data['gameInfo']['visiting-team']['team-code']['id']
    game_type = data['gameInfo']['gametype']['type']
    home_score = data['gameInfo']['home-team-score']['score']
    away_score = data['gameInfo']['visiting-team-score']['score']
    stadium_fox_id = data['gameInfo']['stadium']['id']
    game_code = data['gameInfo']['gamecode']['code']
    total_quarters = data['gameInfo']['total-quarters']['total']
    
    game = nba_db.Game(season=season, game_date=game_date, home_team=home_team, away_team=away_team, game_type=game_type, home_score=home_score, away_score=away_score, stadium=stadium_fox_id, game_code=game_code)
    nba_db.insert_game_foxsports(game)

def parse_player_info(data):
    for p in data:
        first = p['name']['first-name']
        last = p['name']['last-name']
        number = p['player-number']['number']
        player_position = p['player-position']['position']
        primary_position = p['primary-position']['name']
        secondary_position = p['secondary-position']['name']
        foxsports_id = int(p['player-code']['global-id'])
        team_id = int(p['team-code']['id'])
        
        player = nba_db.Player(team_id=team_id, first_name=first, last_name=last, jersey_number=number, primary_position=primary_position, secondary_position=secondary_position, foxsports_id=foxsports_id)
        nba_db.insert_player_foxsports(player)

def parse_personal_info(data):
    home = data['home_team']['nba-player']
    away = data['away_team']['nba-player']
    for p in home:
        p['team_id'] = int(data['home_team']['team-code']['id'])
    for p in away:
        p['team_id'] = int(data['away_team']['team-code']['id'])
    
    players = home
    players.extend(away)
    
    for p in players:
        first = p['name']['first-name']
        last = p['name']['last-name']
        number = p['player-number']['number']
        primary_position = p['primary-position']['name']
        secondary_position = p['secondary-position']['name']
        foxsports_id = int(p['player-code']['global-id'])
        team_id = int(p['team_id'])
        weight = p['weight']['pounds']
        height = p['height']['inches']
        experience = p['experience']['experience']
        school = p['school']['school']
        first_year = p['first-year']['year']
        age = p['age']
        
        player = nba_db.Player(team_id=team_id, first_name=first, last_name=last, jersey_number=number, primary_position=primary_position, secondary_position=secondary_position, foxsports_id=foxsports_id, weight=weight, height=height, experience=experience, age=age, first_year=first_year, school=school)
        nba_db.insert_player_foxsports(player)

def parse_json_data(data):
    insert_into_db.insert_into_db(data)
    parse_player_info(data['playerInfo'])
    parse_personal_info(data['personalInfo'])
    parse_game_info(data)

def parse_dir(onetwosee_dir="./webpages/onetwosee_2015/"):
    files = os.listdir(onetwosee_dir)
    files = glob(os.path.join(onetwosee_dir, '*.json'))
    total = len(files)
    index = 0
    
    for index, json_file in enumerate(files, 1):
        sys.stdout.write("\rParsing %d/%d" % (index, total))
        sys.stdout.flush()
        
        if ".json" in json_file[-5:]:
            #with open(onetwosee_dir + json_file) as open_file:
            with open(json_file) as open_file:
                data = open_file.read()
                json_object = json.loads(data)
                parse_json_data(json_object)
    
    sys.stdout.write("\rCompleted %d/%d\n" % (index, total))
    sys.stdout.flush()

def download_games(games_dir="../data/onetwosee_season_2014/"):
    games = nba_db.get_scheduled_games()
    print("Scraping", str(len(games)), "games. Press ctrl-c to stop early.")
    try:
        for g in games:
            date = list(map(int,g['game_date'].split('-')))
            home = int(g['home_team_id'])
        
            file_code = "%d%02d%02d" % (date[0], date[1], date[2])
            game_code = file_code + "%02d" % home
            cur_url = "http://api.nba.onetwosee.com/update/" + game_code
            file_name = file_code + '_' + team_id_name[home] + '.json'
            path_name = games_dir + file_name
            if not os.path.exists(path_name):
                print("downloading:", file_name)
                try:
                    urllib.request.urlretrieve(cur_url, path_name)
                    time.sleep(1)
                except urllib.request.URLError:
                    print("Error  :", file_name)
            else:
                print("exists:", file_name)
    except KeyboardInterrupt:
        print("Scraping ended early by user.")
        if os.path.exists(path_name):
            os.remove(path_name)


def main():
    pass

if __name__ == '__main__':
    main()
