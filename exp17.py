from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def giveme_kakao_cookie():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('C:/stamp/chromedriver', options=options)

    url = 'https://accounts.kakao.com/login/?continue=https://harmony.kakao.com/auth'

    driver.get(url)
    time.sleep(1)

    id = driver.find_element(By.XPATH, '//*[@id="loginKey--1"]')
    id.send_keys('suhcrates@hanmail.net')
    id = driver.find_element(By.XPATH, '//*[@id="password--2"]')
    id.send_keys('seoseoseo7!')
    time.sleep(10)
    id = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]')
    id.click()
    time.sleep(1)
    driver.get('https://harmony.kakao.com/studio/190/insight/realtime')
    time.sleep(1)
    #
    cookie0 = ''
    # print(driver.get_cookies())
    for dic in driver.get_cookies()[::-1]:
        name0 = dic['name']
        value0 = dic['value']
        cookie0 += f"; {name0}={value0}"
    return cookie0[2:]

giveme_kakao_cookie()