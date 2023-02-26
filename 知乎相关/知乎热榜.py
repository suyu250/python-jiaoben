import requests
import pandas
from bs4 import BeautifulSoup

headers = {
    'cookie': '这里放入你的cookie',
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36',
}
url = 'https://www.zhihu.com/hot'
resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, 'lxml')
contents = soup.find_all('div', class_='HotItem-content')
title_list, hot_list, excerpt_list = [], [], []
for content in contents:
    title = content.find('h2').string
    hot = content.find('div', class_='HotItem-metrics').get_text()
    try:
        excerpt = content.find('p').string
    except AttributeError:
        excerpt = ''
    title_list.append(title)
    hot_list.append(hot.split(' ')[0])
    excerpt_list.append(excerpt)

data = {
    '热度': hot_list,
    '标题': title_list,
    '摘录': excerpt_list,
}
dataframe = pandas.DataFrame(data=data)
dataframe.to_excel('./Table/知乎热榜.xlsx', index=False, encoding='utf-8')

# @time 2021/12/24 2:10
# @author Baneik
# @file 知乎热榜.py
