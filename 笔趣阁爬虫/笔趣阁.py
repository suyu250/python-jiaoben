import os
import requests
from bs4 import BeautifulSoup
from threadpool import ThreadPool, makeRequests


def get_index(url):
    global index_len, novel_name
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    href_list = soup.find('div', id='list').find_all('a')
    num_list = range(1, len(href_list) + 1)
    index_len = len(href_list)
    novel_name = soup.find('h1').string
    index_list = []
    for a_tag, index in zip(href_list, num_list):
        index_list.append('{}-*-https://www.xbiquge.la{}'.format(index, a_tag.get('href')))
    return index_list


def get_content(info):
    url = info.split('-*-')[1]
    num = info.split('-*-')[0]
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    title = soup.find('h1').string
    content = soup.find('div', id='content').get_text().replace('\n\n', '\n').split('亲,点击进去')[0]
    with open('./小说/缓存/{}.txt'.format(num), 'w', encoding='utf-8')as f:
        f.write(title + '\n' + content)


def create_text():
    file = open('./小说/{}.txt'.format(novel_name), 'a', encoding='utf-8')
    for num in range(1, index_len + 1):
        path = './小说/缓存/{}.txt'.format(num)
        content = open(path, 'r', encoding='utf-8').read()
        file.write(content + '\n\n\n')
        os.remove(path)
    print('{}下载完成'.format(novel_name))


headers = {
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
}
index_len = 0
novel_name = 'Novel'

if __name__ == '__main__':
    info_list = get_index(url=input('Url: '))
    pool = ThreadPool(20)
    request = makeRequests(get_content, info_list)
    [pool.putRequest(req) for req in request]
    pool.wait()
    create_text()
