import requests
import time
from db import load_mysql_schema
from player_stats import scrape_player_stats_by_year

def main():
    load_mysql_schema()
    scape_player_stats_by_year(2017)

if __name__ == '__main__':
    main()
