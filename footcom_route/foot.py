# coding = utf-8
import random
import threading
import time
import sys

import pymysql
import requests


from .db.basic_db import get_db_args
from .db.models import FootRoute
from .download.download import Download

args = get_db_args()


class Foot:
    def __init__(self, start_route_id, download_count):
        self.connect = pymysql.connect(host=args['host'], user=args['user'], passwd=args['password'],
                                       db=args['db_name'],
                                       charset='utf8')
        self.cursor = self.connect.cursor()
        self.headers_list = self.read_headers()
        self.start_route_id = start_route_id
        self.download_count = download_count

    def read_headers(self):
        headers_list = []
        # 从mysql读取所有登陆过后的headers
        get_headers_sql = "select * from account order by account.id"
        self.cursor.execute(get_headers_sql)
        results = self.cursor.fetchall()
        for account in results:
            headers = eval(account[4])
            headers_list.append(headers)
        return headers_list

    def download(self):
        print('\n start download-----------------')

        dl = Download()
        dl.session.headers.update(random.choice(self.headers_list))
        for route_id in range(self.start_route_id, self.start_route_id + self.download_count):
            try:
                # 每获取10条route信息就结束session，重新更换一个账号
                if route_id % 10 == 0:
                    dl.session.close()
                    # time.sleep(1)
                    dl.session = requests.session()
                    dl.session.headers.update(random.choice(self.headers_list))

                # 根据route_id查询这条route是否已经抓取过
                res = dl.db_session.query(FootRoute).filter(FootRoute.id == route_id).first()
                if res:
                    print(str(route_id) + ' has been crawled in this turn\n')
                    continue
                else:
                    dl.get_route_info(route_id)
                    # dl.download_file(route_id)
            except Exception as e:
                print(route_id, " not exist\n")

                print(e)
                continue


def download(start, count):
    worker = Foot(start, count)
    worker.download()


if __name__ == '__main__':
    start_id = 2824
    download_count = 20 * 5000
    thread_sum = 20
    offset = int(download_count / thread_sum)
    threads = [threading.Thread(target=download, args=(start_id + i * offset, offset)) for i in range(thread_sum)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
