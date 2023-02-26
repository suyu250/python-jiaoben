import json
import requests
from bs4 import BeautifulSoup
import re
import pandas
import time


def get_cid(url):
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    script = soup.find_all('script')[4].string
    part_list = json.loads(re.findall('"pages":(.*?),"subtitle"', script)[0])
    part_dict = {part['part']: part['cid'] for part in part_list}
    return part_dict


def download_damn(name, oid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(oid)
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    content_list = soup.find_all('d')
    data = {
        'Sender': [],
        'Time': [],
        'Message': [],
    }
    for content in content_list:
        info = content.get('p').split(',')
        data['Time'].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info[4]))))
        data['Message'].append(content.string)
        data['Sender'].append(info[6])
    df = pandas.DataFrame(data)
    df.to_csv('./{}.csv'.format(name), encoding='utf-8-sig', index=False)


def get_damn(url):
    video_dict = get_cid(url)
    for name in video_dict.keys():
        print('正在下载: {}'.format(name))
        download_damn(name=name, oid=video_dict[name])


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3 rv:5.0; bg-BG) AppleWebKit/532.35.5 (KHTML, like Gecko) Version/5.0.5 Safari/532.35.5'
}
get_damn(input('视频链接: '))
