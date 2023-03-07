import traceback
from datetime import datetime
from _donga_one_two_db_maker import _donga_one_two_db_maker
from _donga_newspaper_db_maker import _donga_newspaper_db_maker
from _donga_today_db_maker import _donga_today_db_maker
from _kakao_one_two_db_maker import _kakao_one_two_db_maker
from _naver_one_two_db_maker import _naver_one_two_db_maker
from make_name_db import make_name_db
import mysql.connector


success0 = False
n=0
while not success0 or n >3:
    n+=1
    try:
        config = {
            'user': 'root',
            'password': 'Seoseoseo7!',
            'host': 'localhost',
            # 'database':'shit',
            'port': '3306'
        }

        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        cursor.execute(
            f"""
            update review_auto.crawl_check set try_time = "{datetime.now()}" where ind="1"
            """
        )
        db.commit()


        _donga_one_two_db_maker()
        _donga_today_db_maker()
        _donga_newspaper_db_maker()  # newspaper가 today 다음에 와야함. today의 데이터를 사용해야되기때문
        print('동아 완료')
        _kakao_one_two_db_maker()
        print('다음 완료')
        _naver_one_two_db_maker()
        print('네이버 완료')
        success0 = True


    except Exception:
        cursor.execute(
            f"""
            update review_auto.crawl_check set success0 = 0 where ind="1"
            """
        )
        db.commit()
        print('========fail============')
        traceback.print_exc()

config = {
    'user' : 'root',
    'password': 'Seoseoseo7!',
    'host':'localhost',
    # 'database':'shit',
    'port':'3306'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

cursor.execute(
    f"""
    update review_auto.crawl_check set success0 = 1, success_time = "{datetime.now()}" where ind="1"
    """
)
db.commit()


#### 일 다 끝나면  네임 업데이트
make_name_db()