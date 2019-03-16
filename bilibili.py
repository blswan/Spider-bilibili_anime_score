from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import pymysql
import time
import threading

'''Settings'''
base_url = 'https://www.bilibili.com/anime/index/?spm_id_from=333.334.b_7072696d6172795f6d656e75.13#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page='
table = 'bilibili_anime'
host='localhost'
user='root'
password='abc123456'
port= 3306
database='spiders'
start_page = 1
max_page = 155
threads = 5
sleep_time = 1

def get_index(index_response, db):
	"""
	:index_response 索引页源码
	:db 已连接的数据库
	:video_urls: 为当前页面所有动漫网址
	"""
	video_urls = {}
	index_html = index_response
	index_doc = pq(index_html)
	index_items = index_doc('#app .bangumi-item').items()
	for index_item in index_items:
		index_data = {
			'name': index_item.find('.bangumi-title').text(),
			'shadow': index_item.find('.cover-wrapper .shadow').text(),
			'show_num': index_item.find('.pub-info').text(),
			'video_url': index_item.find('.cover-wrapper').attr('href').strip('//'),
		}
		update_to_mysql(index_data, db)
		anime_url = index_data['video_url']
		anime_name = index_data['name']
		video_urls[anime_name] = anime_url
	return video_urls

def get_detail(detail_response, anime_name, db, sleep_time):
	"""
	:detail_response 动漫播放页面的源码
	:anime_name 动漫名称
	:db 已打开的数据库
	"""
	time.sleep(sleep_time)
	detail_html = detail_response
	detail_doc = pq(detail_html)
	detail_item = detail_doc('#app #bangumi_media')
	score = detail_item.find('.bangumi-media-header .rate-wrapper .rate-score').text()
	detail_data = {
		'name': anime_name,
		'score': score
	}
	update_to_mysql(detail_data, db)

def update_to_mysql(data, db):
	data_keys = ', '.join(data.keys())
	data_values = ', '.join(['%s'] * len(data))
	cursor = db.cursor()
	sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=data_keys, values=data_values)
	update = ','.join([" {key} = %s".format(key=key) for key in data])
	sql += update
	cursor.execute(sql, tuple(data.values())*2)
	db.commit()
	print(f'{data} update successful !')

def open_url(url, located_type, located_element, browser):
	try:
		browser.get(url)
		wait = WebDriverWait(browser, 10)
		wait.until(EC.presence_of_element_located((located_type, located_element)))
	except:
		None
	return browser.page_source

def run(index_url, sem, page, sleep_time):
	db = pymysql.connect(host=host, user=user, password=password, port=port, db=database)
	service_args = []
	service_args.append('--load-images=no')
	service_args.append('--disk-cache=yes')
	browser = webdriver.PhantomJS(service_args = service_args)
	index_page_source = open_url(index_url, By.ID, 'app', browser)
	video_urls = get_index(index_page_source, db)
	for anime_name, anime_url in video_urls.items():
		detail_page_source = open_url('https://' + anime_url, By.CSS_SELECTOR, '#app .bangumi-media-header', browser)
		get_detail(detail_page_source, anime_name, db, sleep_time)
	print('\n==========================')
	print(f"page {page} successful !")
	print('==========================\n')
	time.sleep(sleep_time)
	db.close()
	browser.quit()
	sem.release()

def thread(sem, sleep_time):
	for page in range(start_page, max_page+1):
		index_url = base_url + str(page)
		sem.acquire()
		t = threading.Thread(target=run, args=(index_url,sem, page, sleep_time))
		t.start()



if __name__ == '__main__':
	sem = threading.Semaphore(threads)
	thread(sem, sleep_time)
