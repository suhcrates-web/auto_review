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
    # kakao_cookie="webid=d544c2c97f394519994dfaa028d31fa7; webid_ts=1677421858871; TIARA=eSI5cOoegEL316gP7ark3WnaSyreyzSmJ2njf9xMopMoCaKw9kufA9uUq5N59HrF8DBwtrHZBlofgbzX4y6i9BMDHrHFkzM1UlMdgcZ5fj10; _T_ANO=IglUfjPa5vNv5VHI3FVHdvz5hsidyv54dOamm5aCv9+s2N6tb+aI4MlTVrK5EEv5rxmf0G5ZTEwuvFbHGLgFO7VhR3cdGAmrEf2Wit1MU1SQxTNXEgRJBrupz2pnYGXW1u4FontLmRW5rL6GwejdbfOeXWXlgvme778aM82OTkFbvZlMEYHHQ3+bSfd8RYWztHNoNZNcYkJdXeschOnqDZQmpZpUu82dVng8v6K3jCwHZx1lOl5YgCuHFcjws0CzyiJWI4AsMdvAnPm1FaMDN0AlGfPSygxQ+0Rtyou6eYDlldW/QE8ptYOWFz314/OIB8I5ccVkluKajrr4rBtkQw==; _kawlt=afCP6kwGKqkZ5mR4yb5SRP7UXSetM_yjYlpTBUHwk3rdpDptd8kYZx59lLNSY_BzhSoezrxp8JKW3mTa0DgawxXbE9BwBhdfQ0zZ9d8OJdJBJxViQpG5lcYkOYZXWBQw; _kawltea=1677534459; _karmt=bMTRYdMdd4m7ZJ1W73w6NmF1fGxhjzWALURvCuL8cK2Of4hZ344Md61BCn7TtnAJ; _karmtea=1677545259; _kahai=c337646ae903b3d6bea92b2791c579f0e2b9e0c7bdcba54e1cf06c6d85fed45d; SESSION=ed50f88c-2624-414b-a189-0519c66de411; JSESSIONID=node0onolg9qu7pfn1q9pwgday15eq559046.node0"
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