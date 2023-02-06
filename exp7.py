## 동아
import requests
import json
url= 'https://manage.donga.com/log/view/log.view.php?h=news.donga.com&d=648&rand=1675043301'


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
print(temp.content.decode())
# print(json.loads(temp.content))
