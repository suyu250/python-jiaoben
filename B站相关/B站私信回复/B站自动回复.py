import time
import json
import requests


def send_message(uid, content):
    data = {
        'msg[sender_uid]': my_uid,
        'msg[receiver_id]': uid,
        'msg[receiver_type]': '1',
        'msg[msg_type]': '1',
        'msg[msg_status]': '0',
        'msg[content]': '{{"content":"{}"}}'.format(content),
        'msg[timestamp]': str(time.time())[:10],
        'msg[new_face_version]': '0',
        'msg[dev_id]': msg_id,
        'from_firework': '0',
        'build': '0',
        'mobi_app': 'web',
        'csrf_token': csrf,
        'csrf': csrf,
    }
    headers = {
        'cookie': cookie,
        'origin': 'https://message.bilibili.com',
        'referer': 'https://message.bilibili.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
    }
    url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'
    resp = requests.post(url, headers=headers, data=data).json()
    if resp['code'] == 0:
        return True
    else:
        return False


def get_new_session():
    begin_ts = str(time.time()).replace('.', '')[:-1]
    while True:
        params = {
            'begin_ts': begin_ts,
            'build': '0',
            'mobi_app': 'web',
        }
        headers = {
            'cookie': cookie,
            'origin': 'https://message.bilibili.com',
            'referer': 'https://message.bilibili.com/',
            'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
        }
        get_new_follow()
        url = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?'
        resp = requests.get(url, headers=headers, params=params).json()
        session_list = resp['data']['session_list']
        if not session_list:
            time.sleep(4)
            continue
        for session in session_list:
            message_key = session['last_msg']['msg_key']
            if message_key in msg_key_list:
                continue
            uid = session['talker_id']
            begin_ts = session['session_ts']
            message = json.loads(session['last_msg']['content'])['content']
            timestamp = session['last_msg']['timestamp']
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
            sender = uid
            if uid == my_uid:
                sender = 'Me'
            log = 'Time: {}\nMessage_key: {}\nSender: {}\nMessage: {}\n\n'.format(time_, message_key, sender, message)
            with open('./????????????/????????????/{}.txt'.format(uid), 'a', encoding='utf-8')as f:
                f.write(log)
            with open('./????????????/????????????.txt', 'a')as k:
                k.write('{}-'.format(message_key))
            msg_key_list.append(message_key)
            print('uid: {} -*- Time: {} -*- message: {}'.format(uid, time_, message.replace('\n', '')))

            """
            ???????????????????????????????????????
            """
            if message == '??????':
                send_message(uid=uid, content='Gitee??????: https://gitee.com/bilibili_autumn_leaves/b-station-code')
            elif message == '1':
                send_message(uid=uid, content='Gitee??????: https://gitee.com/bilibili_autumn_leaves/b-station-code')

        time.sleep(4)


def get_new_follow():
    params = {
        'vmid': my_uid,
        'pn': '1',
        'ps': '100',
        'order': 'desc',
        'order_type': 'attention',
        'jsonp': 'jsonp',
    }
    headers = {
        'cookie': cookie,
        'origin': 'https://message.bilibili.com',
        'referer': 'https://message.bilibili.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
    }
    url = 'https://api.bilibili.com/x/relation/followers?'
    resp = requests.get(url, headers=headers, params=params).json()
    follow_li = resp['data']['list']
    for follow in follow_li:
        mid = str(follow['mid'])
        if mid not in follow_list:
            send_message(mid, content=first_follow_message)
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print('UID: {} -*- Time: {} -*- Send: ????????????'.format(mid, time_))
            with open('./????????????/????????????.txt', 'a')as f:
                f.write('{}-'.format(mid))
            follow_list.append(mid)
            time.sleep(0.3)


my_uid = ''
csrf = ''
msg_id = ''

cookie = open('./????????????/Cookie.txt', 'r').read()
file_1 = open('./????????????/????????????.txt', 'r').read()
file_2 = open('./????????????/????????????.txt', 'r').read()

msg_key_list = file_1.split('-')
follow_list = file_2.split('-')

first_follow_message = '??????????????????,??????????????????????????????\\n?????? 1 ?????? ?????? ????????????????????????'

print('---????????????----')
get_new_session()