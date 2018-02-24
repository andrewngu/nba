import requests
import time
from db import load_mysql_schema
from player_stats import scrape_player_stats_by_year
from team_stats import scrape_team_stats_by_year

def main():
    load_mysql_schema()

    for i in range(20):
        year = 2012 - i
        print '============================='
        print 'scraping data for %s...' % year
        scrape_team_stats_by_year(year)
        scrape_player_stats_by_year(year)
        print '=============================\n'

if __name__ == '__main__':
    main()
