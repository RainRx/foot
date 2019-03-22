# -*- coding: utf-8 -*-
import os
file_path = os.path.abspath(os.path.dirname(os.getcwd()))


def get_user_agent():
    agent_list = []
    f = open(file_path + '\\footcom_route\\agent\\user-agent.txt', "rb")
    data = f.readlines()
    for agent in data:
        agent_list.append(agent.decode('utf-8').strip())
    return agent_list

