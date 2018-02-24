import requests
from constants import request_headers
from db import cur, db
from utils import get_year_string


def fetch_player_stats_by_year(year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=' + year_string + '&SeasonType=Regular+Season&StatCategory=PTS'
    r = requests.get(url, headers=request_headers)
    json_result = r.json()
    headers = select_player_stats_columns(json_result['resultSet']['headers'])
    rows = json_result['resultSet']['rowSet']
    return (headers, rows)


def load_player_stats_schema(headers):
    query = '''
CREATE TABLE IF NOT EXISTS `player_stats` (
    `player_id` int(16) NOT NULL,
    `year` int(4) NOT NULL,
    '''

    for header in headers:
        query += '`%s` float,' % (header.lower())

    query += '''
    PRIMARY KEY (`player_id`, `year`)
) ENGINE=InnoDB
    '''
    cur.execute(query)


def insert_player_stats(headers, player_id, stats, year):
    query = 'INSERT IGNORE INTO player_stats (player_id, year,'
    query += ', '.join(headers)
    query += ') VALUES (%d, %d,'
    query += ', '.join('%f' for x in headers)
    query += ')'
    values = (player_id, year) + tuple(stats)
    cur.execute(query % values)
    db.commit()


def insert_player_stats_by_year(headers, rows, year):
    load_player_stats_schema(headers)
    for row in rows:
        player_id = row[0]
        team_abbreviation = row[3]
        stats = select_player_stats_columns(row)
        insert_player_stats(headers, player_id, stats, year)


def scrape_player_stats_by_year(year):
    print 'scraping player stats for %s...' % str(year)
    headers, rows = fetch_player_stats_by_year(year)
    insert_player_stats_by_year(headers, rows, year)


def select_player_stats_columns(arr):
    return arr[4:]
