import requests
from constants import request_headers
from db import cur, db


def fetch_game_details(game_id):
    url = 'https://stats.nba.com/stats/boxscoresummaryv2?GameID=' + game_id
    r = requests.get(url, headers=request_headers)
    result_json = r.json()
    if 'resultSets' in result_json:
        for result_set in result_json['resultSets']:
            if result_set['name'] == 'GameSummary':
                row = result_set['rowSet'][0]
                return row
    return None


def insert_game_details(game_id, row):
    query = 'INSERT IGNORE INTO game (id, date, home_team_id, visitor_team_id) VALUES ("%s", "%s", %d, %d)'
    values = (game_id, row[0], row[6], row[7])
    cur.execute(query % values)
    db.commit()


def scrape_game_details(game_id, team_name, year):
    print 'scraping details for %s %s game %s' % (year, team_name, game_id)
    row = fetch_game_details(game_id)
    if row is not None:
        insert_game_details(game_id, row)
