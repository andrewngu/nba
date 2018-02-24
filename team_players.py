import requests
from constants import request_headers
from db import cur, db
from utils import get_year_string

def fetch_team_players(team_id, year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=' + year_string + '&TeamID=' + str(team_id)
    r = requests.get(url, headers=request_headers)
    result_json = r.json()
    for result_set in result_json['resultSets']:
        if result_set['name'] == 'CommonTeamRoster':
            rows = result_set['rowSet']
            return rows


def insert_team_players(rows, team_id, year):
    for row in rows:
        names = row[3].split(' ')
        first = names[0]
        last = ' '.join(names[1:])

        query = 'INSERT IGNORE INTO player (id, first, last, num, position, height, weight, birthday, school) VALUES (%d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'
        values = (row[12], first, last, row[4], row[5], row[6], row[7], row[8], row[11])
        cur.execute(query % values)
        db.commit()

        query = "INSERT IGNORE INTO player_team_rel (player_id, team_id, year) VALUES (%d, %d, %d)"
        values = (row[12], team_id, year)
        cur.execute(query % values)
        db.commit()


def scrape_team_players(team_id, team_name, year):
    print 'scraping team players for %s %s...' % (year, team_name)
    rows = fetch_team_players(team_id, year)
    insert_team_players(rows, team_id, year)
