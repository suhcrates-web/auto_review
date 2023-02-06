import requests
import json
from bs4 import BeautifulSoup
import time
from giveme_naver_cookie import giveme_naver_cookie

#### 쿠키 가져와서

naver_cookie = giveme_naver_cookie()
# print(naver_cookie)

url = 'https://news-stat-admin.navercorp.com/api/today?timeDimension=DATE&startDate=2023-01-29&section=total&device=TOTAL&channelMainTabType=ALL&_=1673680541938_61180'

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
headers2 = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
'cache-control': 'max-age=0',
'cookie': 'NNB=4YQOEI3TEPAWG; BMR=; VISIT_LOG_CLEAN=1',
'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

temp = requests.get(url, headers=headers)
# print(temp.content)
rows = json.loads(temp.content.decode())['result']['statDataList'][1]['data']['rows']
# print(rows['title'])
print(rows)
# time.sleep(3)
#
# for n in range(len(rows['uri'])):
#     uri = rows['uri'][n]
#     date0 = rows['date'][n]
#     cv = rows['cv_p'][n]
#     title = rows['title'][n]
#     temp = requests.get(uri, headers=headers2)
#     temp = BeautifulSoup(temp.content, 'html.parser')
#     article = temp.find('div', {'id':'newsct_article'})
#     article = article.text.replace('\n','')
#     print(article)
#
#     time.sleep(5)