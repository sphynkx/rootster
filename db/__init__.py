import pymysql
from config import MYSQL_CONFIG

def get_db():
    return pymysql.connect(**MYSQL_CONFIG, cursorclass=pymysql.cursors.DictCursor)

