import requests
import pandas
import os


def get_org_id(code):
    data = {
        'keyWord': code,
        'maxNum': '10',
    }
    url = 'http://www.cninfo.com.cn/new/information/topSearch/query?'
    resp = requests.post(url, data=data, headers=headers)
    for li in resp.json():
        category = li['category']
        if category != 'A股':
            continue
        org_id = li['orgId']
        chin_py = li['zwjc']
        return org_id, chin_py
    return None


def get_file_list(code, org_id, time_se):
    page = 1
    data = {
        'stock': '{},{}'.format(code, org_id),
        'tabName': 'fulltext',
        'pageSize': '30',
        'pageNum': page,
        'column': 'szse',
        'category': '',
        'plate': 'sz',
        'seDate': time_se,
        'searchkey': '',
        'secid': '',
        'sortName': '',
        'sortType': '',
        'isHLtitle': 'true',
    }
    file_dict = {}
    while True:
        url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
        resp = requests.post(url, headers=headers, data=data).json()
        print('Page: {} -*- TotalPages: {}'.format(page, resp['totalpages']))
        for item in resp['announcements']:
            item_type = item['adjunctType']
            if item_type != 'PDF':
                continue
            file_dict[item['announcementTitle']] = 'http://static.cninfo.com.cn/' + item['adjunctUrl']
        if page >= resp['totalpages']:
            break
        page += 1
    return file_dict


def download_pdf(code, time_se, url):
    if not os.path.exists('./file/{}'.format(code)):
        os.makedirs('./file/{}'.format(code))
    if not os.path.exists('./file/{}/{}'.format(code, time_se)):
        os.makedirs('./file/{}/{}'.format(code, time_se))
    resp = requests.get(url, headers=headers).content
    file_name = url.split('/')[-1]
    with open('./file/{}/{}/{}'.format(code, time_se, file_name), 'wb')as k:
        k.write(resp)


def run(code, year):
    org_id, zw = get_org_id(code)
    print('Org_ID: ', org_id)
    year = int(year)
    time_se = '{}-01-01~{}-12-31'.format(year, year)
    print('Time_SE', time_se)
    url_dict = get_file_list(org_id=org_id, code=code, time_se=time_se)
    for title in url_dict.keys():
        download_pdf(url=url_dict[title], time_se=year, code=code)


headers = {
    'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36',
}
df = pandas.read_excel('./stockyr.xlsx', converters={'Stkcd': str, 'Year': str})
df_dict = dict(zip(df['Stkcd'], df['Year']))
for cod in df_dict.keys():
    run(code=cod, year=df_dict[cod])
