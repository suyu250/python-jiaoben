import requests
from bs4 import BeautifulSoup


def download_zh(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    resp = requests.get(url, headers=headers).text
    soup = BeautifulSoup(resp, 'lxml')
    title = soup.find('h1', class_='Post-Title').string
    content = soup.find('div', class_='Post-RichText').get_text()
    with open('./{}.txt'.format(title), 'w', encoding='utf-8')as k:
        k.write(content)


download_zh(url='https://zhuanlan.zhihu.com/p/447416179')
