import MySQLdb
from warnings import filterwarnings

filterwarnings('ignore', category = MySQLdb.Warning)
db = MySQLdb.connect(
    host='192.168.99.100',
    user='root',
    passwd='root',
    db='nba',
)
cur = db.cursor()
schemas = {}

schemas['game'] = '''
CREATE TABLE IF NOT EXISTS `game` (
    `id` varchar(16) NOT NULL,
    `date` varchar(128) NOT NULL,
    `time` varchar(128) NOT NULL,
    `home_team_id` int(16) NOT NULL,
    `visitor_team_id` int(16) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
'''

schemas['game_player_stats'] = '''
CREATE TABLE IF NOT EXISTS `game_player_stats` (
    `game_id` varchar(16) NOT NULL,
    `player_id` int(16) NOT NULL,
    `start_position` varchar(8),
    `comment`varchar(256),
    `min` varchar(16),
    `fgm` float,
    `fga` float,
    `fg_pct` float,
    `fg3m` float,
    `fg3a` float,
    `fg3_pct` float,
    `ftm` float,
    `fta` float,
    `ft_pct` float,
    `oreb` float,
    `dreb` float,
    `reb` float,
    `ast` float,
    `stl` float,
    `blk` float,
    `to` float,
    `pf` float,
    `pts` float,
    `plus_minus` float,
    PRIMARY KEY (`game_id`, `player_id`)
) ENGINE=InnoDB
'''

schemas['game_team_stats'] = '''
CREATE TABLE IF NOT EXISTS `game_team_stats` (
    `game_id` varchar(16) NOT NULL,
    `team_id` int(16) NOT NULL,
    `min` varchar(16),
    `fgm` float,
    `fga` float,
    `fg_pct` float,
    `fg3m` float,
    `fg3a` float,
    `fg3_pct` float,
    `ftm` float,
    `fta` float,
    `ft_pct` float,
    `oreb` float,
    `dreb` float,
    `reb` float,
    `ast` float,
    `stl` float,
    `blk` float,
    `to` float,
    `pf` float,
    `pts` float,
    `plus_minus` float,
    PRIMARY KEY (`game_id`, `team_id`)
) ENGINE=InnoDB
'''

schemas['player'] = '''
CREATE TABLE IF NOT EXISTS `player` (
    `id` int(16) NOT NULL,
    `first` varchar(128) NOT NULL,
    `last` varchar(128) NOT NULL,
    `num` varchar(8),
    `position` varchar(8),
    `height` varchar(8),
    `weight` varchar(8),
    `birthday` varchar(64),
    `school` varchar(128),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
'''

schemas['player_team_rel'] = '''
CREATE TABLE IF NOT EXISTS `player_team_rel` (
    `player_id` int(16) NOT NULL,
    `team_id` int(16) NOT NULL,
    `year` int(4) NOT NULL,
    PRIMARY KEY (`player_id`, `team_id`, `year`)
) ENGINE=InnoDB
'''

schemas['team'] = '''
CREATE TABLE IF NOT EXISTS `team` (
    `id` int(16) NOT NULL,
    `name` varchar(128) UNIQUE NOT NULL,
    `abbreviation` varchar(8),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB
'''

def load_mysql_schema():
    cur.execute(schemas['game'])
    cur.execute(schemas['game_player_stats'])
    cur.execute(schemas['game_team_stats'])
    cur.execute(schemas['player'])
    cur.execute(schemas['player_team_rel'])
    cur.execute(schemas['team'])
