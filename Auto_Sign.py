# -*- coding: utf-8 -*-
import re
import json
import hashlib
import requests
def sign(name, cookies, bduss):
    SIGN_URL = 'http://c.tieba.baidu.com/c/c/forum/sign'
    tbs = get_tbs(cookies, name)
    fid = get_fid(name)
    sign_string = 'BDUSS=%sfid=%dkw=%stbs=%stiebaclient!!!' % (bduss, fid , name, tbs.encode('utf-8'))
    sign_md5 = hashlib.md5(sign_string).hexdigest().upper()
    data = {
        'BDUSS':bduss,
        'fid':fid,
        'kw':name,
        'tbs':tbs.encode('utf-8'),
        'sign':sign_md5
    }

    #print type(sign_md5)

    sign_request = requests.post(SIGN_URL, data=data)
    '''
    pattern_sign = re.compile(r'"errno":(\d+?),')
    try:
        status = pattern_sign.search(sign_request.text).group(1)
    except:
        status = 'unknown error'
    '''
    status = sign_request.text
    #print status
    return 'Sign Status %s' %(status)

def get_tbs(cookies, name):
    TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
    tbs_request = requests.get(TBS_URL, cookies=cookies)
    pattern_tbs = re.compile(r'"tbs":"(.+?)",')
    tbs = pattern_tbs.search(tbs_request.text).group(1)
    return tbs

def get_fid(name):
    url = 'http://tieba.baidu.com/f/commit/share/fnameShareApi?ie=utf-8&fname=%s' % name
    fid_request = requests.get(url)
    fid_json = json.loads(fid_request.content)
    fid = fid_json['data']['fid']
    #print type(fid)
    return fid