import re
import requests
from bs4 import BeautifulSoup

headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/77.0.3865.120 Safari/537.36"
    }

url = 'https://www.haodf.com/hospital/DE4raCNSz6Omic7eSMfL7SHT.htm'

# 获取内容
res = requests.get(url, headers=headers)
html = res.text

html = BeautifulSoup(html, 'lxml')

# print(html)

orange = re.findall(r'"h-i-orange">(.+?)</span>', str(html))

print(orange)
