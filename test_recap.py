# NBA NLP - Senior Project - Spring 2015
# Recap Generator - Testing
# Jacob Bustamante

"""
test_recap
This is used to quickly generate the specified test_games articles.
The chosen games represent a variety of games and should be used to efficently test
the quality of the recap generator.
"""

import sys, os
import gen_recap
from gen_recap import gen_article
from data import nba_db

web_file_dir = "./web/2014_season/"
test_games = [1, 8, 121, 300, 500, 640, 641, 646, 800, 801, 1220, 1225]

def generate_web_article(game_id, open_browser=True, partial=False):
    partial_time = (3, 8, 0)
    gen_article(game_id, partial, partial_time)
    if open_browser:
        os.system("open " + web_file_dir + str(nba_db.get_game_code(game_id)) + ".html")

def main():
    if len(sys.argv) < 1:
        print("Usage: python3 test_recap.py")
    open_browser = False if "q" in sys.argv else True
    partial = True if "partial" in sys.argv else False

    for game_id in test_games:
        generate_web_article(game_id, open_browser, partial)

if __name__ == '__main__':
    main()
