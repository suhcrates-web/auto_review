from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def giveme_naver_cookie():
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument("disable-gpu")
    driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)

    url ='https://friend.navercorp.com/login/loginForm.sec?url='

    driver.get(url)
    time.sleep(1)

    id = driver.find_element(By.XPATH, '//*[@id="user_id"]')
    id.send_keys('FRA10360')
    id = driver.find_element(By.XPATH, '//*[@id="user_pw"]')
    id.send_keys('donga#2022')
    id = driver.find_element(By.XPATH, '//*[@id="btn-login"]')
    id.click()
    time.sleep(1)
    driver.get('https://pub-iims.navercorp.com/view/svc/main?svcId=MIS&lz=ko_KR&tz=Asia%2FSeoul%3A%2B09%3A00')
    time.sleep(1)
    # id = driver.find_element(By.XPATH, '//*[@id="carousel"]/div[1]/ul/li[3]/div/a')
    # id.click()
    # time.sleep(1)
    # id = driver.find_element(By.XPATH, '//*[@id="menu"]/li[3]/ul/li[6]/a')
    # id.click()
    # time.sleep(1)
    driver.get('https://news-stat-admin.navercorp.com/api/rank/article/cv?timeDimension=DATE&startDate=2023-01-14&section=total&device=TOTAL&channelMainTabType=ALL&_=1673860219308_48249')

    cookie0 = ''
    for dic in driver.get_cookies()[::-1]:
        name0 = dic['name']
        value0 = dic['value']
        cookie0 += f"; {name0}={value0}"

    return cookie0


