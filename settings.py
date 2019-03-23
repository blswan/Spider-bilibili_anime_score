# settings of mysql connection
TABLE = 'bilibili_anime'
HOST = 'localhost'
USER = 'root'
PASSWORD = 'abc123456'
PORT = 3306
DATABASE = 'spiders'

# spider's start & end
START_PAGE = 1
END_PAGE = 156

# sleep time between each request
SLEEP_TIME = 2

# speed of request
THREADS = 3

# the type of anime to be extracted
REQUIREMENT = 'score>9.0'