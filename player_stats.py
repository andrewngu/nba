import requests
from db import cur, db
from utils import get_year_string


def fetch_player_stats_by_year(year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=' + year_string + '&SeasonType=Regular+Season&StatCategory=PTS'
    r = requests.get()
    json_result = r.json()
    headers = json_result['resultSet']['headers']
    rows = json_result['resultSet']['rowSet']
    return (headers, rows)


def insert_player_stats_by_year(headers, rows):
    print headers, rows


def scape_player_stats_by_year(year):
    json_result = fetch_player_stats_by_year(year)
    parse_player_stats(json_result)
