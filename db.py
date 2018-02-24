import MySQLdb

db = MySQLdb.connect(
    host='192.168.99.100',
    user='root',
    passwd='root',
    db='nba',
)
cur = db.cursor()
schemas = {}
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

schemas['team'] = '''
CREATE TABLE IF NOT EXISTS `team` (
    `id` int(16) NOT NULL,
    `name` varchar(128) UNIQUE NOT NULL,
    `abbreviation` varchar(8),
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


def load_mysql_schema():
    cur.execute(schemas['player'])
    cur.execute(schemas['team'])
    cur.execute(schemas['player_team_rel'])
