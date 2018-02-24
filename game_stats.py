import requests
from constants import request_headers
from db import cur, db


def insert_game_player_stats(game_id, row):
    if row[8] != None:
        query = 'INSERT IGNORE INTO game_player_stats (game_id, player_id, start_position, comment, min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, `to`, pf, pts, plus_minus) VALUES ("%s", %d, "%s", "%s", "%s", %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f)'
        values = (game_id, row[4]) + tuple(row[6:])
        cur.execute(query % values)
        db.commit()


def insert_game_team_stats(game_id, row):
    query = 'INSERT IGNORE INTO game_team_stats (game_id, team_id, min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, `to`, pf, pts, plus_minus) VALUES ("%s", %d, "%s", %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f)'
    values = (game_id, row[1]) + tuple(row[5:])
    cur.execute(query % values)
    db.commit()


def scrape_game_stats(game_id, team_name, year):
    print 'scraping stats for %s %s game %s' % (year, team_name, game_id)
    url = 'https://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=' + game_id + '&RangeType=0&Season=2011-12&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
    r = requests.get(url, headers=request_headers)
    result_json = r.json()

    for result_set in result_json['resultSets']:
        if result_set['name'] == 'PlayerStats':
            for row in result_set['rowSet']:
                insert_game_player_stats(game_id, row)

        if result_set['name'] == 'TeamStats':
            for row in result_set['rowSet']:
                insert_game_team_stats(game_id, row)
