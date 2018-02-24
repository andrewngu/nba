import requests
import time
from constants import request_headers
from db import cur, db
from game import scrape_games_by_year
from team_details import scrape_team_details
from team_players import scrape_team_players
from utils import get_year_string


def fetch_team_stats_by_year(year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=' + year_string + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
    r = requests.get(url, headers=request_headers)
    json_result = r.json()
    headers = map(
        lambda x: x.lower(),
        select_team_stats_columns(json_result['resultSets'][0]['headers']),
    )
    rows = json_result['resultSets'][0]['rowSet']
    return (headers, rows)


def insert_team_stats_by_year(headers, rows, year):
    load_team_stats_schema(headers)
    for row in rows:
        team, team_stats = parse_team_row(row)
        scrape_team_details(team['id'], team['name'])
        insert_team_stats(headers, team, team_stats, year)
        scrape_team_players(team['id'], team['name'], year)
        scrape_games_by_year(team['id'], team['name'], year)
        time.sleep(2)


def insert_team_stats(headers, team, team_stats, year):
    query = 'INSERT IGNORE INTO team_stats (team_id, year,'
    query += ', '.join(headers)
    query += ') VALUES (%d, %d,'
    query += ', '.join('%f' for x in headers)
    query += ')'
    values = (team['id'], year) + tuple(team_stats)
    cur.execute(query % values)
    db.commit()


def load_team_stats_schema(headers):
    query = '''
CREATE TABLE IF NOT EXISTS `team_stats` (
    `team_id` int(16) NOT NULL,
    `year` int(4) NOT NULL,
    '''

    for header in headers:
        query += '`%s` float,' % (header.lower())

    query += '''
    PRIMARY KEY (`team_id`, `year`)
) ENGINE=InnoDB
    '''
    cur.execute(query)


def parse_team_row(row):
    team = {'id': row[0], 'name': row[1]}
    team_stats = select_team_stats_columns(row)
    return (team, team_stats)


def scrape_team_stats_by_year(year):
    print "scraping team stats for %s..." % str(year)
    headers, rows = fetch_team_stats_by_year(year)
    insert_team_stats_by_year(headers, rows, year)


def select_team_stats_columns(arr):
    return arr[2:-1]
