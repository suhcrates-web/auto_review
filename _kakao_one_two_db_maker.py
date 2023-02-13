from database import cursor, db
import requests
import json
from bs4 import BeautifulSoup
import time
from datetime import date, timedelta
from giveme_kakao_cookie import giveme_kakao_cookie
from collections import defaultdict

import mysql.connector

def _kakao_one_two_db_maker():
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
        """
        drop table if exists review_auto.kakao_one_two
        """
    )

    cursor.execute(
        """
        create table if not exists review_auto.kakao_one_two(
        date0 date,
        title0 varchar(100),
        cv int
        )
        """
    )


    #### 쿠키 가져와서
    try:
        kakao_cookie = giveme_kakao_cookie()
    except:
        kakao_cookie = giveme_kakao_cookie()

    #### 1~2일 전꺼
    yest0 = date.today() - timedelta(days= 1)
    yest00 =  date.today() - timedelta(days= 2)
    url = f'https://harmony.kakao.com/proxy/insight/pv/best/range/{yest00.strftime("%Y%m%d")}-{yest0.strftime("%Y%m%d")}/media/total?size=200&includeVodInfo=true'
    # print(url)

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
        'cookie': kakao_cookie,
        'referer': 'https://harmony.kakao.com/studio/190/insight/contents?startDate=20230127&endDate=20230128',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }



    temp = requests.get(url, headers=headers)
    # print(temp.content)
    rows = json.loads(temp.content.decode())

    dics = {}
    for row in rows:
        # print(row)
        date0 = str(row['regDt'])[:8]
        cv = row['pv']
        title0 = row['title']
        if title0 == None:
            break
        title0 = title0.replace('"', '“')
        title_shrunk = title0.replace(' ','')

        dics[title_shrunk] = {'date0':date0, 'cv':cv, 'title0':title0}


    for i in dics:
        cursor.execute(
            f"""
            insert into review_auto.kakao_one_two values("{dics[i]['date0']}" ,"{dics[i]['title0']}", "{dics[i]['cv']}") 
            """
        )
    db.commit()

    ### 오늘꺼 실시간
    cursor.execute(
        """
        drop table if exists review_auto.kakao_today
        """
    )

    cursor.execute(
        """
        create table if not exists review_auto.kakao_today(
        date0 date,
        title0 varchar(100),
        cv int
        )
        """
    )

    url = f'https://harmony.kakao.com/proxy/insight/pv/best/range/{date.today()}-{date.today()}/media/total?size=200&includeVodInfo=true'

    temp = requests.get(url, headers=headers)
    # print(temp.content)
    rows = json.loads(temp.content.decode())

    dics = {}
    for row in rows:
        # print(row)
        date0 = str(row['regDt'])[:8]
        cv = row['pv']
        title0 = row['title']
        if title0 == None:
            break
        title0 = title0.replace('"', '“')
        title_shrunk = title0.replace(' ', '')

        dics[title_shrunk] = {'date0': date0, 'cv': cv, 'title0': title0}

    for i in dics:
        cursor.execute(
        f"""
            insert into review_auto.kakao_today values("{dics[i]['date0']}" ,"{dics[i]['title0']}", "{dics[i]['cv']}") 
            """
        )
    db.commit()