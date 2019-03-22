import hashlib
import json
import os
import time
from datetime import datetime

import requests

from db.basic_db import Session
from db.tables import route_info

file_path = os.path.abspath(os.path.dirname(os.getcwd()))

TIMEOUT = 1


class Download:
    def __init__(self):
        self.session = requests.session()
        self.db_session = Session()

    def generate_proxy(self):
        ip = "forward.xdaili.cn"
        port = "80"

        # 订单号
        orderno = "ZF2019346340NVPU17"

        secret = "46c515a121c84a0ba7d24997b6f1a7fa"

        ip_port = ip + ":" + port
        timestamp = str(int(time.time()))  # 计算时间戳
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()  # 计算sign
        sign = md5_string.upper()  # 转换成大写
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        headers = {"Proxy-Authorization": auth}
        return proxy, headers

    def get_real_url(self, download_url):
        response = self.session.get(download_url)
        return response.history[-1].url

    def download_file(self, route_id):
        download_url = "http://www.foooooot.com/trip/%d/download/?fileformat=kml" % route_id
        real_url = self.get_real_url(download_url)
        data = self.session.get(real_url).content
        print(data)
        if data and ("六只脚" not in str(data)):
            file_name = file_path + '\\footcom_route\\data\\data_{}.kml'.format(route_id)
            with open(file_name, 'wb') as f:
                f.write(data)
                f.close()
            print("{} kml success\n".format(route_id))
            time.sleep(TIMEOUT)
        else:
            print("%d不存在或被封ip" % route_id)

    def get_route_info(self, route_id):
        proxy, headers = self.generate_proxy()
        # 以下为3个目标url
        off_set_track_json_url = 'http://www.foooooot.com/trip/{}/offsettrackjson/'.format(route_id)
        off_set_footprints_url = 'http://www.foooooot.com/trip/{}/offsetfootprintsjson/'.format(route_id)
        info_url = 'http://www.foooooot.com/client2/trip/{}/info/'.format(route_id)

        # off_set_track_json以json文件的形式存储，后续建立索引
        off_set_track_json_response = self.session.get(url=off_set_track_json_url,
                                                       headers=headers,
                                                       proxies=proxy,
                                                       timeout=500,
                                                       verify=False,
                                                       allow_redirects=False).content.decode('utf-8')
        off_set_track_json = json.loads(off_set_track_json_response)
        file_name = file_path + '\\footcom_route\\data\\data_{}_off_set_track.json'.format(route_id)
        with open(file_name, 'w') as f:
            f.write(str(off_set_track_json))
            f.close()
        print("{} off_set_track_json success".format(route_id))
        time.sleep(TIMEOUT)

        # info 直接存入MySQL
        info_response = self.session.get(url=info_url,
                                         headers=headers,
                                         proxies=proxy,
                                         timeout=500,
                                         verify=False,
                                         allow_redirects=False).content.decode('utf-8')
        info = json.loads(info_response)['data']

        # 修改时间戳等数据格式
        info['edit_timestamp'] = datetime.fromtimestamp(info['edit_timestamp']).strftime("%Y-%m-%d %H:%M")
        info['occurtime'] = datetime.fromtimestamp(info['occurtime']).strftime("%Y-%m-%d %H:%M")
        info['create_time'] = datetime.fromtimestamp(info['create_time']).strftime("%Y-%m-%d %H:%M")
        info['info_last_update'] = datetime.fromtimestamp(info['info_last_update']).strftime("%Y-%m-%d %H:%M")
        info['track_last_update'] = datetime.fromtimestamp(info['track_last_update']).strftime("%Y-%m-%d %H:%M")
        # bool转换为0/1
        info['has_footprint'] = 0 if info['has_footprint'] is False else 1
        info['own'] = 0 if info['own'] is False else 1
        info['is_collected'] = 0 if info['is_collected'] is False else 1
        info['mark_addible'] = 0 if info['mark_addible'] is False else 1
        # 时间sec转换为min
        info['duration'] = round(info['duration'] / 60 - 0)

        # 构造sql语句，一次插入info字典中所有键值对
        insert_sql = route_info.insert().values(info)
        self.db_session.execute(insert_sql)
        self.db_session.commit()
        time.sleep(TIMEOUT)

        # off_set_footprints以json文件的形式存储，后续建立索引
        off_set_footprints_response = self.session.get(url=off_set_footprints_url,
                                                       headers=headers,
                                                       proxies=proxy,
                                                       verify=False,
                                                       timeout=500,
                                                       allow_redirects=False).content.decode('utf-8')
        off_set_footprints = json.loads(off_set_footprints_response)
        file_name = file_path + '\\footcom_route\\data\\data_{}_off_set_footprints.json'.format(route_id)
        with open(file_name, 'w') as f:
            f.write(str(off_set_footprints))
            f.close()
        print("{} off_set_footprints success".format(route_id))
        time.sleep(TIMEOUT)
