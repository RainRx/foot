# coding:utf-8
import os
import random
from yaml import load

config_path = os.path.join(os.path.dirname(__file__), 'conf.yaml')


with open(config_path) as f:
    cont = f.read()

cf = load(cont)


def get_db_args():
    return cf.get('db')