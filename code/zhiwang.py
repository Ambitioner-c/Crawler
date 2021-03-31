# coding=utf-8
# @Author: cfl
# @Time: 2021/3/30 21:11

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re
from random import randint
import requests
from selenium.webdriver.common.keys import Keys


if __name__ == '__main__':

    # 加载谷歌驱动
    driver = webdriver.Chrome("E:\\Driver\\chromedriver.exe")
    driver.maximize_window()

    # 打开空间首页
    driver.get("https://kns.cnki.net/kns8/defaultresult/index")
    sleep(randint(2, 4))

    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
    }
    Data = {'keyword': 'cnn',
            }
    # # 获取filename
    # html = requests.post('https://wap.cnki.net/touch/web/Article/Search', headers=Headers, data=Data,)
    # html = html.text
    # print(html)

    # # 获取详情页面
    # html = requests.get('https://kns.cnki.net/kcms/detail/detail.aspx'
    #                     '?dbcode=CAPJ'
    #                     '&dbname=CAPJLAST'
    #                     '&filename=JSJA2021011100Q',
    #                     headers=Headers)
    # html = html.text
    # print(html)
    url = 'https://kns.cnki.net/kcms/detail/detail.aspx' \
          '?dbcode=CAPJ' \
          '&dbname=CAPJLAST' \
          '&filename=HNNB20210326000'
    driver.get(url)

    #  frame1架构
    driver.switch_to.frame('frame1')
    sleep(randint(2, 4))
    html = driver.page_source
    html = BeautifulSoup(html, 'lxml')
    # print(html)

    # 下一页
    driver.find_element_by_xpath("//a[contains(text(),'下一页')]").send_keys('\n')
    # #  frame1架构
    # driver.switch_to.frame('frame1')
    # sleep(randint(2, 4))
    html2 = driver.page_source
    html2 = BeautifulSoup(html2, 'lxml')
    print(html2)

    # 通过href检索
    # href = html.findAll('a', attrs={'class': 'Mark'})[0]
    # href = re.findall(r'href="(.+?)">', str(href))[0]
    # href = str(href).replace('amp;', '')
    # print(href)
    #
    # # html = requests.get(href, headers=Headers)
    # # html = html.text
    # # print(html)
    # driver.get(href)
    # html = driver.page_source
    # html = BeautifulSoup(html, 'lxml')
    # print(html)

    # driver.close()
