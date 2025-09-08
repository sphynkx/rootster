import pymysql
from config import MYSQL_CONFIG, EDITABLE_FIELDS, PERMIT_DELETE_EXCLUDE_TABLES


def get_db():
    return pymysql.connect(**MYSQL_CONFIG, cursorclass=pymysql.cursors.DictCursor)

