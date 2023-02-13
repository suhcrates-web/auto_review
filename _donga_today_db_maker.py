from database import cursor, db
from datetime import date, timedelta
import requests
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict

import mysql.connector

def _donga_today_db_maker():

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
        drop table if exists review_auto.donga_today
        """
    )

    cursor.execute(
        """
        create table if not exists review_auto.donga_today(
        date0 date,
        title0 varchar(100),
        cv int,
        url varchar(100)
        )
        """
    )


    url= f'https://manage.donga.com/start/data.matrix.php?media=NEWS&symd=00000000&eymd=00000000&c=all&l=300&c1=&refer='


    headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'legoauth=6%2Bvr6%2B3i6er42Pjo2Mjo2MjYmLj46Bi5OKwtLc1dzT0YuThlI0IVgpMVAhBl4JAYuTjoGLk4%2BNjISAnYyAnY%2BNnI6HjoSHiIqBi5ON%2BfT69Pns8fv0%2F%2B7p4YuTgYuTgYuTg%3D',
    'Host': 'manage.donga.com',
    'Referer': 'https://manage.donga.com/start/start.php',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }

    temp = requests.get(url, headers=headers)

    temp = BeautifulSoup(temp.content, 'html.parser')
    # print(temp)
    titles = temp.findAll('td', {'class':'title'})
    cvs = temp.findAll('td', {'class':'cnt'})
    dates = temp.findAll('td', {'class':'date'})

    for i in range(len(titles)):
        # print(titles[i].text)
        # print(titles[i].find('a')['href'])
        # print(dates[i].text)
        # print(cvs[i].text)
        url_code = re.findall(r'(?<=/)\d+(?=/)', titles[i].find('a')['href'])
        xl_url = url_code[-2] + '/' + url_code[-1]
        cursor.execute(
            f"""
                insert into review_auto.donga_today values("{dates[i].text}" ,"{titles[i].text.replace('○','').replace('△','')}", "{cvs[i].text.replace(',','')}", "{xl_url}")
                """
        )
    db.commit()
_donga_today_db_maker()