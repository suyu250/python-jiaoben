import time
import requests
import simplejson.errors


def get_video_list(mid):
    url = 'https://api.bilibili.com/x/space/arc/search?'
    page = 1
    video_aid_list = []
    params = {
        'mid': mid,
        'ps': '30',
        'tid': '0',
        'pn': page,
        'keyword': '',
        'order': 'pubdate',
        'jsonp': 'jsonp',
    }
    while True:
        res = requests.get(url=url, headers=headers, params=params).json()
        video_list = res['data']['list']['vlist']
        video_count = res['data']['page']['count']
        for video in video_list:
            video_aid_list.append(video['aid'])
        if page * 30 >= video_count:
            return video_aid_list
        page += 1


def give_love(aid):
    url = 'https://api.bilibili.com/x/web-interface/coin/add'
    data = {
        'aid': aid,
        'multiply': '1',
        'select_like': '1',
        'cross_domain': 'true',
        'csrf': 'ae92e9c2d4b44115050bd201e24b074e',
    }
    try:
        resp = requests.post(url, headers=headers, data=data).json()
    except simplejson.errors.JSONDecodeError:
        print('服务器回复异常,建议检查cookie和mid是否正常')
        return
    code = resp['code']
    if code == 0:
        print('aid: {} 投币成功'.format(aid))
    elif code == 34005:
        print('aid: {} 超出投币上限'.format(aid))


def start_auto_coin(uid):
    av_list = get_video_list(mid=uid)
    for av in av_list:
        give_love(aid=av)
        time.sleep(2)


if __name__ == '__main__':
    headers = {
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com',
        'cookie': '',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
    }
    start_auto_coin(uid=input('输入UID: '))
