# coding = utf-8
import requests
import urllib.request
import random
import time
from footcom_route.agent.user_agent import get_user_agent
from footcom_route.proxy.proxy import get_proxy
MAX_RETRY = 3


def login(user, password):
    login_status = 0
    session = requests.session()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "www.foooooot.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random.choice(get_user_agent())
    }

    session.headers.update(headers)

    try_num = 0
    while login_status == 0 and try_num < MAX_RETRY:
        try:
            login_url = 'http://www.foooooot.com/accounts/login/'
            index_url = 'http://www.foooooot.com/'

            # 【请求】login页，获取csrftoken
            session.get(url=login_url)
            time.sleep(1)
            csrftoken = session.cookies['csrftoken']
            headers['Cookie'] = 'csrftoken=' + csrftoken

            data = {
                "csrfmiddlewaretoken": csrftoken,
                "email": user,
                "password": password,
                "next": "/accounts/login_complete/",
            }

            # 【请求】post登陆数据
            res = session.post(url=login_url, data=data, headers=headers)
            status_code = res.status_code
            if status_code == 200:
                res2 = session.get(url=index_url)
                index_status_code = res2.status_code
                # index = res2.content.decode('utf-8')
                if index_status_code == 200:
                    login_status = 1
                    session_id = session.cookies['sessionid']
                    headers['Cookie'] += '; sessionid=' + session_id
                    print('{} login complete'.format(str(user)))
                    return str(headers)
        except BaseException as e:
            session.close()
            time.sleep(1)
            session = requests.session()
            headers['User-Agent'] = random.choice(get_user_agent())
            try_num += 1
            print(e)
    print('login {} failed'.format(str(user)))
    return ''