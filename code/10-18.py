from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pymysql
import time

db = pymysql.connect('127.0.0.1', 'root', 'cfl656359504', 'crawler')
cursor = db.cursor()

# url = 'https://k.autohome.com.cn/4851/#pvareaid=3454440'

chrome_opt = Options()  # 创建参数设置对象.
chrome_opt.add_argument('--headless')  # 无界面化.
chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)  #不加载图片
chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
chrome_opt.add_argument("--no-sandbox") #使用沙盒模式运行

# 创建Chrome对象并传入设置信息.
driver = webdriver.Chrome(executable_path='/home/cfl/chromedriver/chromedriver', chrome_options=chrome_opt)

url = 'https://k.autohome.com.cn/detail/view_01djezkw7c68vk2d1h6wr00000.html?st=2&piap=0|4851|0|0|1|0|0|0|0|0|1#pvareaid=2112108'
# rs = requests.get(url)

driver.get(url)
sleep(randint(1, 3))

html = driver.page_source
html = BeautifulSoup(html, 'lxml')

div = html.findAll('div', attrs={'class': 'review-main commentParentBox'})

for i in div:
    name = re.findall(r'user-name.+?</i>(.+?)</a>', str(i))[0]
    name = str(name).lstrip()
    review = re.findall(r'review-cont.+?>(.+?)<div', str(i))[0]
    review = str(review).lstrip()
    floor = re.findall(r'font-arial.+?>(.+?)</span>', str(i))
    if len(floor) == 2:
        relation = str(floor[1])
    else:
        relation = ''

    # print(name)
    # print(review)
    # print(floor)
    sql = 'INSERT INTO crawler.date(ID,USERNAME,REVIEW,FLOOR,RELATION) VALUES ("%s","%s","%s","%s","%s")' % (str(time.time()), str(name), str(review), str(floor[0]), str(relation))
    cursor.execute(sql)
    db.commit()

print('第1页完成！')


for i in range(11):
    # 第i+1页
    driver.find_element_by_class_name('page-item-next').click()
    sleep(randint(1, 3))

    html = driver.page_source
    html = BeautifulSoup(html, 'lxml')

    div = html.findAll('div', attrs={'class': 'review-main commentParentBox'})

    for j in div:
        name = re.findall(r'user-name.+?</i>(.+?)</a>', str(j))[0]
        name = str(name).lstrip()
        review = re.findall(r'review-cont.+?>(.+?)<div', str(j))[0]
        review = str(review).lstrip()
        floor = re.findall(r'font-arial.+?>(.+?)</span>', str(j))
        if len(floor) == 2:
            relation = str(floor[1])
        else:
            relation = ''

        sql = 'INSERT INTO crawler.date(ID,USERNAME,REVIEW,FLOOR,RELATION) VALUES ("%s","%s","%s","%s","%s")' % (str(time.time()), str(name), str(review), str(floor[0]), str(relation))
        cursor.execute(sql)
        db.commit()

    print('第%s页完成！' % str(i+2))

db.close()

driver.quit()
