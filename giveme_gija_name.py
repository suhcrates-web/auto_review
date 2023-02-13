import requests
from bs4 import BeautifulSoup

def giveme_gija_name(url):

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'd=63e9825409b9d2739e10; _gid=GA1.2.933289823.1676247638; dable_uid=4375585.1676103948280; ACEFCID=UID-63E98261DB803512C131BF00; cs=cGZzOjJ8; trc_cookie_storage=taboola%2520global%253Auser-id%3D3CF9C69266296FD923EAD427673C6EAD; __gads=ID=a08bd50a3c211a5d-22ffba71c5d90035:T=1676247648:S=ALNI_MYzFaU1Le6aRJI3iPijMGms9wSIvA; __igaw__adid=MDAwPThmNzFmYTI3LWFiM2QtMTFlZC05Mzc3LTAyNDJhYzExMDAwMg==; _pubcid=c653a665-28bf-413d-a87d-48b23cfb510d; _cc_id=a307227bc8c71c4fa95f5c9b6a01568b; panoramaId_expiry=1676856441010; panoramaId=9e37421dea0df90772adf506490916d53938c90264c75c10b6ffbd715da6717a; searchWord=%5B%22%5Cuc9c0%5Cuba74%22%5D; gourl=https%3A%2F%2Fwww.donga.com%2Fnews%2FEconomy%2Farticle%2Fall%2F20230213%2F117853282%2F1%3Fref%3Dmain; sns_naver_state=884e01293ceb5b1809e212c20201e90d; donga_sns_naver=6%2Bvr6u7v7er42Pjo2PjI6MjI2KiI2Bi5OI0tyA3cLv18Pe1%2BL61tbfhY3rhdGLk4jr5ML7zIDZ%2FPLRi5OMiIiOiI2FiIGLk4GLk4GLk47Ixd7fzNnI3s313NPQ3NTR05PY2cGLk4rlhY%2Fw9ern59D%2Fwvbbw%2FrUh%2BGLk4GLk4GLk4XZyc3Ox4KSmsrKw5nS09rc057S0NKT2NrOwpj%2B0tPS0NTCnN%2FJxN7R2NKc0dHSn42Pjo2PjI6CnIyKhYiOj4WPgpyCj8jb0IDc1NPQ%3D%3D; donga_login=naver; tscookie=15535085; dongauserid=15535085; dongausernick=swater; sns_login=naver; dongauseremail=suhcrates%40hanmail.net; suhcratesdongacom=1; joinus=117853282%2C117851434%2C117851237; pepdongacom=1; nowdongacom=1; 71wookdongacom=1; legoauth=6%2Bvr6%2B3i6e742Pjo2PjI6MiYyJj4uBi5OKwtLc1dzT0YuThlI0IVgpMVAhBl4JAYuTjoGLk4%2BNjISAnYyAnY%2BNnI6HjoSHiIqBi5ON%2BfT69Pns8fv0%2F%2B7p4YuTgYuTgYuTg%3D; _gat_UA-59562926-1=1; _ga_6Z5MY0NF20=GS1.1.1676268671.4.1.1676269252.0.0.0; _ga=GA1.2.1887394565.1676247638; __gpi=UID=00000bc0b2734197:T=1676247648:RT=1676269253:S=ALNI_MYJBV6Hx-v8aSEmnnZeK3LBCuZ1SA; cto_bundle=NpjLdV8lMkJhWGx2YjhraUEwZm9jZGU2bzVneDIlMkJiU3c2Z0ZDOUdPY09DajluN0YxdEJydyUyRjJFV1NoM0Fxcjhhb1hPMGRjSWY1eiUyQnZWenJhaWUzWms0aE5VJTJGb0RhSm95S0xSNnNVdHI1NnBRTzZOTzFtclNzR21scXh1cWNEd3Y5dHpBRkZteEUwNkFXeVVWbEhNVmtleHFrSUZ3JTNEJTNE; donga_dceid=FltCQ29bQl9vW0JDJ1tsQ2FZUkMuXHwiLlx8I2xyQX58dXtQJkxOWFd3UVBjdEFQZnRVI2NMTkcuXHwibltSYXtGfGF7Rnxhe0Z8X2FbfFNuW1JXJEZVTz11JXJ%2BclFAb0ZVTz1GVU89QXxhe0Z8X25bVSJuW0JDY1tCQyJafFMkRlVPPVt8V29bbFdvW0JbblhCX25GVU89dHtQJExOX2NPJC9i%00; cst=d3BwOjEzfA%3D%3D',
    'Host': 'www.donga.com',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    print(f'https://www.donga.com/news/article/all/{url}')
    temp = requests.get(f'https://www.donga.com/news/article/all/{url}')
    temp = BeautifulSoup(temp.content, 'html.parser')
    return temp.find('div', {'class':'report'}).findAll('a')[0].text.replace('기자','').replace(' ','')