import random
import time
import requests
from B站评论爬取 import get_reply

headers = {
    'cookie': '需要填入自己的cookie',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com',
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
}


def give_like(rpid):
    data = {
        'oid': '722199672',
        'type': '1',
        'rpid': rpid,
        'action': '1',
        'ordering': 'heat',
        'jsonp': 'jsonp',
        'csrf': '2af12e2f5e5f42e144f3df423e2e8bdb',
    }
    url = 'https://api.bilibili.com/x/v2/reply/action'
    res = requests.post(url, headers=headers, data=data).json()
    if res['code'] == 0:
        print('{}: 点赞成功!'.format(rpid))
    else:
        print('{}: 有点问题?'.format(rpid))


def run(url):
    aid = get_reply(url)
    lines = open('./table/{}.csv'.format(aid), 'r', encoding='utf-8').read().split('\n')
    for line in lines:
        try:
            int(line.split(',')[0])
        except (TypeError, ValueError):
            continue
        rpid_ = line.split(',')[0]
        give_like(rpid=rpid_)
        time.sleep(random.uniform(0.1, 1.5))


run(url=input('URL: '))
