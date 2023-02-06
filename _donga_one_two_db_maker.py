from database import cursor, db
from datetime import date, timedelta
import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict


cursor.execute(
    """
    drop table if exists review_auto.donga_one_two
    """
)

cursor.execute(
    """
    create table if not exists review_auto.donga_one_two(
    date0 date,
    title0 varchar(100),
    cv int,
    url varchar(100)
    )
    """
)

yest0 = date.today() - timedelta(days= 1)
yest00 =  date.today() - timedelta(days= 2)

url= f'https://manage.donga.com/start/data.matrix.php?media=TOTAL.NEWS&symd={yest00.strftime("%Y%m%d")}&eymd={yest0.strftime("%Y%m%d")}&c=all&l=all&c1=&refer='


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

article_list = []

temp = requests.get(url, headers=headers)

temp = BeautifulSoup(temp.content, 'html.parser')
div0 = temp.find('div', {'class':'matrixList'})
trs = temp.findAll('tr')
for tr in trs[1:-1]:
    url0 = tr.find('a')['href']
    tds = tr.findAll('td')
    temp = []
    for td in tds[1:]:
        temp.append(td.text)
    article_list.append((temp, url0))

for temp, url0 in article_list:
    title0 = temp[0].replace('△','').replace('○','').replace('"','“')
    date0 = temp[1][:10].replace('.','')
    cv = temp[4].replace(',','')

    cursor.execute(
        f"""
            insert into review_auto.donga_one_two values("{date0}" ,"{title0}", "{cv}", "{url0}")
            """
    )
db.commit()