import time
import requests
from MessageBot import send_robot_message


def get_my_follow():
    url = 'https://api.bilibili.com/x/relation/tag?'
    page = 1
    params = {
        'mid': '2011670789',
        'tagid': '427747',
        'pn': page,
        'ps': '20',
        'jsonp': 'jsonp',
    }
    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3 rv:5.0; bg-BG) AppleWebKit/532.35.5 (KHTML, like Gecko) Version/5.0.5 Safari/532.35.5'
    }
    while True:
        resp = requests.get(url, headers=headers, params=params).json()
        data = resp['data']
        for dt in data:
            mid = str(dt['mid'])
            if mid in follow_list:
                return
            else:
                with open('./info/follow_list.txt', 'a', encoding='utf-8')as k:
                    k.write('{}-'.format(mid))
                follow_list.append(mid)
        page += 1


def get_new_video(mid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3 rv:5.0; bg-BG) AppleWebKit/532.35.5 (KHTML, like Gecko) Version/5.0.5 Safari/532.35.5'
    }
    params = {
        'mid': mid,
        'ps': '30',
        'tid': '0',
        'pn': 1,
        'keyword': '',
        'order': 'pubdate',
        'jsonp': 'jsonp',
    }
    url = 'https://api.bilibili.com/x/space/arc/search?'
    resp = requests.get(url=url, headers=headers, params=params).json()
    new_video = resp['data']['list']['vlist'][0]['bvid']
    if new_video not in videos_list:
        up_name = resp['data']['list']['vlist'][0]['author']
        up_uid = resp['data']['list']['vlist'][0]['mid']
        video_title = resp['data']['list']['vlist'][0]['title']
        send_robot_message(up_name=up_name, up_uid=up_uid, video_name=video_title, video_url=new_video)
        videos_list.append(new_video)
        with open('./info/videos_list.txt', 'a')as k:
            k.write('{}-'.format(new_video))
    time.sleep(1)


def init():
    _cookie = open('./info/cookie.txt', 'r').read()
    _follow_list = open('./info/follow_list.txt', 'r').read().split('-')
    _videos_list = open('./info/videos_list.txt', 'r').read().split('-')
    _follow_list.remove('')
    _videos_list.remove('')
    return _cookie, _follow_list, _videos_list


if __name__ == '__main__':
    cookie, follow_list, videos_list = init()
    while True:
        get_my_follow()
        [get_new_video(follow) for follow in follow_list]
