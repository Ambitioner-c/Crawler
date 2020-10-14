from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re
from random import randint
import pymysql


def login(u, p):
    driver.find_element_by_id('login_div')

    # login_frame架构
    driver.switch_to.frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').send_keys(u)
    driver.find_element_by_id('p').send_keys(p)
    driver.find_element_by_id('login_button').click()
    driver.switch_to.default_content()
    sleep(randint(2, 4))


def get_info(u):
    list_ = []

    url = 'https://user.qzone.qq.com/' + u + '/main'
    driver.get(url)
    sleep(randint(2, 4))
    for num in range(1, 300):
        print(num)
        driver.execute_script('window.scrollBy(0, 5000)')
        sleep(randint(2, 4))
    driver.find_element_by_id('QM_Feeds_Container')

    #  QM_Feeds_Iframe架构
    driver.switch_to.frame('QM_Feeds_Iframe')
    sleep(randint(15, 30))
    html = driver.page_source
    html = BeautifulSoup(html, 'lxml')

    ul = html.findAll('ul', attrs={'id': 'host_home_feeds'})[0]
    li = ul.findAll('li', attrs={'class': re.compile(r'f-single')})
    for li_i in li:
        qq = li_i.findAll('div', attrs={'class': re.compile('f-nick')})[0].get_text()

        time = li_i.findAll('div', attrs={'class': re.compile('info-detail')})[0].get_text()

        try:
            # info = re.findall(r'f-info">(.+?)</div>', str(li_i))[0]
            info = li_i.findAll('div', attrs={'class': re.compile('f-info')})[0].get_text()
        except:
            info = 'info_None'
            print(info)

        try:
            # phone = re.findall(r'来自.+?>(.+?)</a>', str(li_i))[0]
            phone = li_i.findAll('a', attrs={'class': re.compile('phone-style')})[0].get_text()
        except:
            phone = 'phone_None'
            print(phone)

        try:
            # like = re.findall(r'f-like-cnt">(\d+)</span>', str(li_i))[0]
            like = li_i.findAll('span', attrs={'class': re.compile('f-like-cnt')})[0].get_text()
        except:
            like = 'like_None'
            print(like)

        try:
            # visitor = re.findall(r'Visitor">(.+?)</a>', str(li_i))[0]
            visitor = li_i.findAll('a', attrs={'data-role': re.compile('Visitor')})[0].get_text()
        except:
            visitor = 'visitor_None'
            print(visitor)

        # 评论
        try:
            com_ul = li_i.findAll('div', attrs={'class': re.compile('comments-list')})[0]
            comments = com_ul.findAll('div', attrs={'class': re.compile('comments-content')})
            comment = ''
            for cmt_i in comments:
                card = re.findall(r'qq\.com/(\d+)', str(cmt_i))[0]

                text = re.findall(r'</a>(.+?)<div', str(cmt_i))[0]
                text = str(text).strip()
                text = re.sub(r'<.+?>', '', text)

                state = re.findall(r'state">(.+?)</span>', str(cmt_i))[0]

                comment += str(card) + '|' + text + '|' + str(state) + '。'
        except:
            comment = 'com_None'
            print(comment)

        list_.append((str(qq), str(time), str(info), str(phone), str(like), str(visitor), comment))

    driver.switch_to.default_content()

    return list_


def insert(list_):
    for ist_i in list_:
        try:
            # 插入数据
            cursor.execute('insert into info values(%s, %s, %s, %s, %s, %s, %s)',
                           (ist_i[0], ist_i[1], ist_i[2], ist_i[3], ist_i[4], ist_i[5], ist_i[6]))
            db.commit()
        except:
            print("重复插入")
            continue

        print(ist_i[0] + "||" + ist_i[1] + "||" + ist_i[2] + "||" + ist_i[3] +
              "||" + ist_i[4] + "||" + ist_i[5] + "||" + ist_i[6])


if __name__ == '__main__':
    # 打开数据库
    db = pymysql.connect("localhost", "root", "123456", "qq")
    cursor = db.cursor()

    # 加载谷歌驱动
    driver = webdriver.Chrome("E:\\driver\\chromedriver.exe")
    driver.maximize_window()

    # 打开空间首页
    driver.get("https://i.qq.com")
    sleep(randint(2, 4))

    user = '656359504'
    password = 'cuifulai123'

    # 登录
    login(user, password)

    # 获取信息
    info_list = get_info('2845308721')

    # 插入数据库
    insert(info_list)

    driver.close()
