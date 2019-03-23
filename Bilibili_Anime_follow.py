import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from lxml import etree
import settings

host = settings.HOST
user = settings.USER
password = settings.PASSWORD
port = settings.PORT
database = settings.DATABASE
table = settings.TABLE
requirement = settings.REQUIREMENT
anime = []


def get_anime_list():
    db = pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        db=database)
    cursor = db.cursor()
    sql = 'SELECT name, video_url FROM %s WHERE %s' % (table, requirement)
    try:
        cursor.execute(sql)
        print('Count:', cursor.rowcount)
        row = cursor.fetchone()
        while row:
            anime.append(row)
            row = cursor.fetchone()
    except BaseException:
        print('Error')
    else:
        print("动漫列表：\n", anime)


def follow_anime(browser):
    for i in range(0, len(anime)):
        url = anime[i][1]
        browser.get('https://' + url)
        html = etree.HTML(browser.page_source)
        try:
            real_url = html.xpath('//*[@id="bangumi_detail"]//div[@class="info-title clearfix"]/a/@href')[0].strip(
                '//') or html.xpath('//*[@id="media_module"]//div[@class="media-right"]/a/@href')[0].strip('//')
        except BaseException:
            None
        browser.get('https://' + real_url)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app"]//div[@class="bangumi-btn"]')))
        time.sleep(1)
        try:
            follow_button = browser.find_element_by_xpath(
                '//*[@id="app"]//div[@class="btn-follow"]')
            follow_button.click()
        except NoSuchElementException:
            print('此番已追，过！')


if __name__ == '__main__':
    """浏览器打开后有10秒的登陆时间"""
    get_anime_list()
    browser = webdriver.Chrome()
    browser.get('https://passport.bilibili.com/login')
    time.sleep(10)
    follow_anime(browser)
    browser.quit()
