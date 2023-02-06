from database import cursor, db
import requests
import json
from bs4 import BeautifulSoup
import time
from datetime import date, timedelta
from giveme_naver_cookie import giveme_naver_cookie
from collections import defaultdict


cursor.execute(
    """
    drop table if exists review_auto.naver_one_two
    """
)

cursor.execute(
    """
    create table if not exists review_auto.naver_one_two(
    date0 date,
    title0 varchar(100),
    cv int,
    createDateTime timestamp
    )
    """
)


#### 쿠키 가져와서
try:
    naver_cookie = giveme_naver_cookie()
except:
    naver_cookie = giveme_naver_cookie()
dics = {}

n =0
for days0 in [2,1]: ## 순서 1,2에서 2,1로 바꿈.  기사 A가 2일전, 1일전에 모두 걸려있을 수 있는데, 1일전 걸 앞세워야 하기때문.
    date0 = date.today() - timedelta(days= days0)
    url = f'https://news-stat-admin.navercorp.com/api/today?timeDimension=DATE&startDate={date0}&section=total&device=TOTAL&channelMainTabType=ALL&_=1673680541938_61180'
    # print(url)

    headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': naver_cookie,
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }



    temp = requests.get(url, headers=headers)
    # print(temp.content)
    rows = json.loads(temp.content.decode())['result']['statDataList'][1]['data']['rows']

    #
    for n in range(len(rows['uri'])):
        uri = rows['uri'][n]
        # date0 = rows['date'][n] # 얘는 그냥 검색날짜. 의미없음
        cv = rows['cv'][n]
        createDate = rows['createDate'][n] #등록 일시
        date0 = createDate[:10]  # 얘가 등록날짜
        title0 = rows['title'][n].replace('"','“')
        title_shrunk = title0.replace(' ','')

        dics[title_shrunk] = {'date0':date0, 'cv':cv, 'title0':title0, 'createDate':createDate}

    if days0 == 1:
        time.sleep(3)


for i in dics:
    cursor.execute(
        f"""
        insert into review_auto.naver_one_two values("{dics[i]['date0']}" ,"{dics[i]['title0']}", "{dics[i]['cv']}", "{dics[i]['createDate']}") 
        """
    )
db.commit()