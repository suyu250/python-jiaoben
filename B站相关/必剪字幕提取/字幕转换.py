import json
import time
import bs4


def b_cut_json_2_bcc(path):
    fd = open('{}/project.xml'.format(path), 'r', encoding='utf-8').read()
    soup = bs4.BeautifulSoup(fd, 'lxml')
    try:
        name = soup.find('footage').get('name').split('/')[-1].split('.')[0]
    except AttributeError:
        name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    json_bcc = {
        "font_size": 0.4,
        "font_color": "#FFFFFF",
        "background_alpha": 0.5,
        "background_color": "#9C27B0",
        "Stroke": "none",
        "type": "AIsubtitle",
        "lang": "zh",
        "version": "r1.2.3.0",
        "body": [],
    }
    sid = 1
    for key in soup.find_all('caption'):
        start = round(int(key.get('inpoint')) / check, 2)
        end = round(start + int(key.get('duration')) / check, 2)
        text = key.get('text')
        body = {
            "from": start,
            "to": end,
            "sid": sid,
            "location": 2,
            "content": text,
        }
        json_bcc['body'].append(body)
        sid += 1
    with open('./{}.bcc'.format(name), 'w')as k:
        json.dump(json_bcc, k)


def b_cut_json_2_srt(path):
    fd = open('{}/project.xml'.format(path), 'r', encoding='utf-8').read()
    soup = bs4.BeautifulSoup(fd, 'lxml')
    try:
        name = soup.find('footage').get('name').split('/')[-1].split('.')[0]
    except AttributeError:
        name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    sid = 1
    fs = open('./{}.srt'.format(name), 'a', encoding='utf-8')
    for key in soup.find_all('caption'):
        start = round(int(key.get('inpoint')) / check, 2)
        end = round(start + int(key.get('duration')) / check, 2)
        text = key.get('text')
        st_hour, st_tmin, st_second = time.localtime(start).tm_hour - 8, time.localtime(start).tm_min, time.localtime(start).tm_sec
        ed_hour, ed_tmin, ed_second = time.localtime(end).tm_hour - 8, time.localtime(end).tm_min, time.localtime(end).tm_sec
        if '{}:{}'.format(st_tmin, st_second) == '{}:{}'.format(ed_tmin, ed_second):
            continue
        st_dec, ed_dec = str(start).split('.')[1], str(end).split('.')[1]
        start_time = '{}:{}:{},{}0'.format(st_hour, st_tmin, st_second, st_dec)
        end_time = '{}:{}:{},{}0'.format(ed_hour, ed_tmin, ed_second, ed_dec)
        line = '{}\n{} --> {}\n{}\n\n'.format(sid, start_time, end_time, text)
        fs.write(line)
        sid += 1


check = 1000000
b_cut_json_2_srt(path='')
b_cut_json_2_bcc(path='')
