# -*- coding: utf-8 -*-
import os
file_path = os.path.abspath(os.path.dirname(os.getcwd()))


def get_proxy():
    proxy_list = []
    f = open(file_path + '\\footcom_route\\proxy\\proxy.txt', "rb")
    data = f.readlines()
    for proxy in data:
        proxy_list.append(proxy.decode('utf-8').strip())
    return proxy_list
