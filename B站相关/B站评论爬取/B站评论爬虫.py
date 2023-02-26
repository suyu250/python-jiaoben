import random
import requests
import time
import re

headers = {
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
}


def get_oid(url):
    resp = requests.get(url, headers=headers).text
    oid = re.findall('"aid":(.*?),', resp)[0]
    return oid


def get_second_reply(rpid, page):
    page_num = 1
    while True:
        params = {
            'jsonp': 'jsonp',
            'pn': page_num,
            'type': '1',
            'oid': aid,
            'ps': '10',
            'root': rpid,
            '_': '1640190856379',
        }
        second_url = 'https://api.bilibili.com/x/v2/reply/reply?'
        resp = requests.get(url=second_url, headers=headers, params=params).json()
        count = resp['data']['page']['count']
        replies = resp['data']['replies']
        for reply in replies:
            reply_create_time = reply['ctime']
            reply_uname = reply['member']['uname']
            reply_content = reply['content']['message'].replace('\n', '').replace(',', '，')
            reply_rpid = reply['rpid']
            line = '{},{},{},{},\n'.format(reply_create_time, reply_uname, reply_content, reply_rpid)
            fd.write(line)
        print('\r当前页码: {} -*- 二级评论: {}'.format(page, page_num), end='')
        time.sleep(random.uniform(0.5, 0.7))
        page_num += 1
        if page_num * 10 >= count:
            break


def get_first_reply():
    page_num = 0
    while True:
        params = {
            'jsonp': 'jsonp',
            'next': page_num,
            'type': '1',
            'oid': aid,
            'mode': '3',
            'plat': '1',
            '_': '1640189054670',
        }
        first_url = 'https://api.bilibili.com/x/v2/reply/main?'
        resp = requests.get(url=first_url, headers=headers, params=params).json()
        print('\r当前页码: {} -* 二级评论: 0'.format(page_num), end='')
        page_num = resp['data']['cursor']['next']
        replies = resp['data']['replies']
        if not replies:
            break
        for reply in replies:
            reply_create_time = reply['ctime']
            reply_uname = reply['member']['uname']
            reply_content = reply['content']['message'].replace('\n', '').replace(',', '，')
            reply_rpid = reply['rpid']
            reply_count = reply['rcount']
            line = '{},{},{},{},\n'.format(reply_create_time, reply_uname, reply_content, reply_rpid)
            fd.write(line)
            if reply_count != 0:
                get_second_reply(rpid=reply_rpid, page=page_num)
        time.sleep(random.uniform(0.2, 0.7))


aid = get_oid(url=input('url: '))
fd = open('./{}.csv'.format(aid), 'a', encoding='utf-8-sig')
fd.write('时间,名称,内容,RPID,\n')
get_first_reply()
