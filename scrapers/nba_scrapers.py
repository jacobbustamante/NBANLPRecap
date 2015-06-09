# NBA NLP - Senior Project - Spring 2015
# Scrapers - Main
# Jacob Bustamante

import os
from glob import glob
import scrapers.scrapers_globals as sg
import scrapers.scrape_onetwosee as scraper
import scrapers.scrape_foxsports as fox_scraper

cur_gamedata_dir = sg.cur_gamedata_dir
cur_gameschedule_dir = sg.cur_gameschedule_dir
parse_dir = scraper.parse_dir

def get_scraper_dir_count(cur_dir="./"):
    filepath = cur_dir + cur_gamedata_dir
    files = glob(os.path.join(filepath, '*.json'))
    total = len(files)
    return total

def get_scraper_schedule_dir_count(cur_dir="./"):
    filepath = cur_dir + cur_gameschedule_dir
    files = glob(os.path.join(filepath, '*.json'))
    total = len(files)
    return total


def import_dir_into_db(cur_dir=cur_gamedata_dir):
    parse_dir(cur_dir)

def import_schedule_dir_into_db(cur_dir=cur_gamedata_dir):
    cur_dir += sg.cur_gameschedule_dir + "/"
    fox_scraper.parse_schedules(cur_dir)


def scrape_game_schedules(cur_dir="./"):
    cur_path = cur_dir + sg.cur_gameschedule_dir + "/"
    fox_scraper.download_schedules_season(schedules_dir=cur_path)

def scrape_games(cur_dir="./"):
    cur_path = cur_dir + sg.cur_gamedata_dir + "/"
    scraper.download_games(games_dir=cur_path)

