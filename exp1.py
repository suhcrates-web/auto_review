import traceback
from datetime import datetime
from _donga_one_two_db_maker import _donga_one_two_db_maker
from _kakao_one_two_db_maker import _kakao_one_two_db_maker
from _naver_one_two_db_maker import _naver_one_two_db_maker
import mysql.connector


success0 = False

config = {
    'user': 'root',
    'password': 'Seoseoseo7!',
    'host': 'localhost',
    'port': '3306'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
cursor.execute(
    """
    select success0, success_time from review_auto.crawl_check where ind ='1'
    """
)

success0, suc_time = cursor.fetchall()[0]
print(success0)
print(suc_time)