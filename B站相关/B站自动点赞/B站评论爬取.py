import random
import requests
import time
import re
from bs4 import BeautifulSoup


# 获取标题和aid
def get_bilibili_oid(b_url):
    fh_list = ['/', '\\', '*', '?', '<', '>', '|', '“', '”']
    try:
        res_video = requests.get(b_url).text
    except():
        return False
    soup_ = BeautifulSoup(res_video, 'lxml')
    oid = re.findall('"aid":(.*?),', res_video)[0]
    tit = soup_.find('span', class_='tit').string
    for t in fh_list:
        tit = tit.replace(t, '')
    return oid, tit


# 获取评论信息
class Bilibili_reply:
    def __init__(self, title):
        self.time_stp = str(time.time()).replace('.', '')[:13]
        self.headers = {
            'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/94.0.4606.61Safari/537.36',
        }
        self.fd = open('./table/{}.csv'.format(title), 'a', encoding='utf-8-sig')
        self.fd.write(head)

    # 获取一级评论
    def get_reply(self, oid, pn):
        params_fr = {
            'jsonp': 'jsonp',
            'next': '{}'.format(pn),
            'type': '1',
            'oid': '{}'.format(oid),
            '_': self.time_stp,
        }
        fr_rep_url = 'https://api.bilibili.com/x/v2/reply/main?'
        try:
            res = requests.get(fr_rep_url, headers=self.headers, params=params_fr, timeout=3).json()
            time.sleep(random.uniform(0.3, 2))
        except():
            time.sleep(random.uniform(0.3, 2))
            return False
        for reply in res['data']['replies']:
            reply_name = reply['member']['uname'].replace(',', '，').replace('\n', '|')
            reply_uuid = reply['member']['mid']
            reply_cont = reply['content']['message'].replace(',', '，').replace('\n', '|')
            reply_time = reply['ctime']
            reply_rcont = reply['rcount']
            reply_rpid = reply['rpid']
            reply_like = reply['like']
            reply_uplk = reply['up_action']['like']
            reply_uprp = reply['up_action']['reply']
            line = '{},{},{},{},{},{},{},{},{}'.format(reply_rpid, reply_name, reply_uuid, reply_cont, reply_time, reply_like, reply_uplk, reply_uprp, '\n')
            self.fd.write(line)
            pn = 1
            print('一级评论: ' + reply_cont)
            if reply_rcont > 0:
                while True:
                    try:
                        self.get_reply_(oid=oid, reply_rpid=reply_rpid, pn=pn)
                        time.sleep(random.uniform(0.1, 0.4))
                        pn += 1
                    except TypeError:
                        time.sleep(random.uniform(0.3, 2))
                        break

    # 获取二级评论
    def get_reply_(self, reply_rpid, oid, pn):
        sd_rep_url = 'https://api.bilibili.com/x/v2/reply/reply?'
        params_sd = {
            'jsonp': 'jsonp',
            'pn': '{}'.format(pn),
            'type': '1',
            'oid': '{}'.format(oid),
            'root': '{}'.format(reply_rpid),
            '_': self.time_stp,
        }
        try:
            res = requests.get(sd_rep_url, headers=self.headers, params=params_sd, timeout=3).json()
        except():
            return False
        for reply in res['data']['replies']:
            reply_name = reply['member']['uname'].replace(',', '，').replace('\n', '|')
            reply_uuid = reply['member']['mid']
            reply_cont = reply['content']['message'].replace(',', '，').replace('\n', '|')
            reply_time = reply['ctime']
            reply_like = reply['like']
            reply_uplk = reply['up_action']['like']
            reply_uprp = reply['up_action']['reply']
            reply_rpid_ = reply['rpid']
            line = '{},{},{},{},{},{},{},{},{}'.format(reply_rpid_, reply_name, reply_uuid, reply_cont, reply_time, reply_like, reply_uplk, reply_uprp, '\n')
            self.fd.write(line)
            print('{}二级评论: '.format(' ' * 8) + reply_cont)


# 运行
def get_reply(url):
    pg = 1
    aid, title = get_bilibili_oid(b_url=url)
    time.sleep(random.uniform(0.1, 0.3))
    freaks = Bilibili_reply(title=aid)
    while True:
        try:
            freaks.get_reply(oid=aid, pn=pg)
            pg += 1
        except TypeError:
            break
    return aid


# 表格头部
head = 'Reply_id,Name,Uid,ReplyCont,ReplyTime,Like,Up-like,Up-reply,\n'

if __name__ == "__main__":
    get_reply(url=input('URL: '))

# @time 2021/12/22 23:19 PM
# @author 几秋残页
# @file B站弹幕信息.py
