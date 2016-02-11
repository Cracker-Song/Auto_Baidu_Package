# -*- coding: utf-8 -*-
import json
import requests


def robot(content, userid):
    key = ‘yourkey’
    robot_url = 'http://www.tuling123.com/openapi/api?key=%s&info=%s&userid=%s' % (key, content, userid)
    robot_request = requests.post(robot_url)#, headers=headers)
    respond_robot = json.loads(robot_request.text)
    code = respond_robot['code']
    if code==100000:
        respond = respond_robot['text']
    elif code==200000:
        respond = '%s  %s ' % (respond_robot['text'], respond_robot['url'])
    elif code==302000:
        respond = '%s\n' % respond_robot['text']
        #print respond_robot
        for news in respond_robot['list']:
            respond += u'标题:%s \n来源:%s \n缩略图:%s \n详细:%s \n' % (news['article'], news['source'], news['icon'], news['detailurl'])
    elif code==308000:
        respond = '%s\n' % respond_robot['text']
        #print respond_robot
        for cook in respond_robot['list']:
            #print type(cook['info'])
            respond += u'菜名:%s \n图片:%s \n做法:%s \n详细:%s\n' % (cook['name'], cook['icon'], cook['info'], cook['detailurl'])
    else:
        respond = code
    return respond
print robot('我想看新闻', 'test')