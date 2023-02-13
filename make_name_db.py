from datetime import date, timedelta
import requests
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict
import time

import mysql.connector

def make_name_db():

    download0 = True
    n=0
    dic = {}
    while download0:
        url = f'https://manage.donga.com/content/content_list.php?p={n}1&iid=94&q=%EA%B8%B0%EC%9E%90&s=&f_category='
        n +=1

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
        for br in temp.find_all("br"):  # 뒷부분을 '소속'을 발라내려고.
            br.replaceWith("\n")
        trs = temp.findAll('table',{'width':'950'})[-1].findAll('tr')[2:-1]

        # for tr in trs:
        #     print("############")
        #     tds = tr.findAll('td')
        #     for td in tds:
        #         print(td.text.split('\n'))
        #         print('============')
        #>>>>>>>
        #  ['3183196', '', '편집']
        # ============
        # ['김지영']
        # ============
        # ['']
        # ============
        # ["'2030세상' 필진입니다."]
        # ============
        # ['호칭: 작가', '소속: 스타트업 투자심사역(VC)·작가', '회사: 사외필진 (3)', '칼럼URL: https://www.donga.com/news/Series/70040100000163', '이메일: ', '생성시간: 2022-02-03 14:31:59', '수정시간: 2022-02-14 17:44:33', '상태: 서비스사용 (6)', '']

        if len(trs) == 0:
            break

        for tr in trs:
            tds = tr.findAll('td')
            name0 = tds[1].text.strip()
            state0 = tds[-1].text.split('\n')
            sosok0 =  state0[1].replace('소속: ','')
            call0 = state0[0].replace('호칭: ','').replace(' ','')
            if call0 == '기자':
                dic[name0] = sosok0



        print(n)
        time.sleep(2)

    ## dic 에 다운로드가 다 끝나면 db에 업로드. 기존 db 빠갰는데 중간에 다운로드 오류나면 안되기때문.
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
        """
        drop table if exists review_auto.name_db
        """
    )

    cursor.execute(
        """
        create table if not exists review_auto.name_db(
        name0 varchar(20),
        sosok0 varchar(100)
        )
        """
    )
    for name0, sosok0 in dic.items():
        cursor.execute(
            f"""
            insert into review_auto.name_db values("{name0}", "{sosok0}")
            """
        )
    db.commit()
