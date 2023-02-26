import requests


def get_video_play_count(mid):
    url = 'https://api.bilibili.com/x/space/arc/search?'
    play_count, page = 0, 1
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
            play_count += video['play']
        if page * 30 >= video_count:
            return play_count
        page += 1


def get_album_view_count(mid):
    url = 'https://api.bilibili.com/x/dynamic/feed/draw/doc_list?'
    view_count, page = 0, 0
    view_id_list = []
    params = {
        'uid': mid,
        'page_num': page,
        'page_size': '30',
        'biz': 'all',
        'jsonp': 'jsonp',
    }
    while True:
        res = requests.get(url, headers=headers, params=params).json()
        items = res['data']['items']
        for item in items:
            if item['doc_id'] in view_id_list:
                return view_count
            view_id_list.append(item['doc_id'])
            view_count += item['view']
        page += 1


headers = {
    'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
}
print(get_video_play_count(mid='1505087845'))
print(get_album_view_count(mid='1505087845'))
