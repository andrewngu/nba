import requests
from constants import request_headers
from db import cur, db

def fetch_team_details(team_id):
    url = 'https://stats.nba.com/stats/teamdetails?teamID=' + str(team_id)
    r = requests.get(url, headers=request_headers)
    json_result = r.json()

    for result_set in json_result['resultSets']:
        if result_set['name'] == 'TeamBackground':
            headers = map(lambda x: x.lower(), result_set['headers'])
            rows = result_set['rowSet']
            return (headers, rows[0])


def insert_team_details(headers, row):
    query = "INSERT IGNORE INTO team (id, name, abbreviation) VALUES (%d, '%s', '%s')"
    values = (row[0], row[2], row[1])
    cur.execute(query % values)
    db.commit()


def scrape_team_details(team_id, team_name):
    print 'scraping team details for %s...' % team_name
    headers, row = fetch_team_details(team_id)
    insert_team_details(headers, row)
