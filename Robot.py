# -*- coding: utf-8 -*-
import json
import requests
headers = {
    'apikey':'fc9e6ac7e5c99cda6eea29ee8fa59f00'
}


def robot(content):
    key = '879a6cb3afb84dbf4fc84a1df2ab7319'
    robot_url = 'http://apis.baidu.com/turing/turing/turing?key=%s&info=%s' % (key, content)
    robot_request = requests.get(robot_url, headers=headers)
    respond_robot = json.loads(robot_request.text)
    respond = respond_robot['text']
    return respond
