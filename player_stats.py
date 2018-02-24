def fetch_player_stats_by_year(year):
    year_string = get_year_string(year)
    url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=' + year_string + '&SeasonType=Regular+Season&StatCategory=PTS'
    r = requests.get()
    return r.json()

def parse_player_stats(json_result):
    headers = json_result['resultSet']['headers']
    rows = json_result['resultSet']['rowSet']

    return (headers, rows)

def scape_player_stats_by_year(year):
    json_result = fetch_player_stats_by_year(year)
    parse_player_stats(json_result)

def store_player_stats_by_year(headers, rows):
    return
