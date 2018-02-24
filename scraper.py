import requests
import time
from db import load_mysql_schema
from team_stats import scrape_team_stats_by_year

def main():
    load_mysql_schema()
    scrape_team_stats_by_year(2017)

if __name__ == '__main__':
    main()
