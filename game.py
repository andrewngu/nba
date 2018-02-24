import requests
from constants import request_headers
from game_details import scrape_game_details
from game_stats import scrape_game_stats
from db import cur, db
from utils import get_year_string


def fetch_games_by_year(team_id, year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/teamgamelog?DateFrom=&DateTo=&LeagueID=00&Season=' +  year_string + '&SeasonType=Regular+Season&TeamID=' + str(team_id)
    r = requests.get(url, headers=request_headers)
    result_json = r.json()
    rows = result_json['resultSets'][0]['rowSet']
    return rows


def scrape_game(game_id, team_name, year):
    scrape_game_stats(game_id, team_name, year)
    scrape_game_details(game_id, team_name, year)


def scrape_game_if_needed(team_name, row, year):
    game_id = row[1]
    cur.execute("SELECT id FROM game WHERE id = %s" % game_id)
    data = cur.fetchall()
    if len(data) == 0:
        scrape_game(game_id, team_name, year)


def scrape_games_by_year(team_id, team_name, year):
    print "scraping games for %s %s" % (year, team_name)
    rows = fetch_games_by_year(team_id, year)
    for row in rows:
        scrape_game_if_needed(team_name, row, year)
