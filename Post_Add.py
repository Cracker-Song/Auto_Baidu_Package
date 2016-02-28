# -*- coding: utf-8 -*-
import re
import hashlib
import requests

def get_tbs(cookies):
    TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
    tbs_request = requests.get(TBS_URL, cookies=cookies)
    pattern_tbs = re.compile(r'"tbs":"(.+?)",')
    tbs = pattern_tbs.search(tbs_request.text).group(1)
    return tbs


def get_fid(name):
    FID_URL = 'http://tieba.baidu.com/f?ie=utf-8&kw=%s&fr=search' % (name)
    fid_request = requests.get(FID_URL)
    pattern_fid = re.compile(r'"forum_id":(\d+?),')
    fid = pattern_fid.search(fid_request.text).group(1)
    #print type(fid)
    return fid

def add(cookies, name, tid, content, bduss, type):
    tbs = get_tbs(cookies).encode('utf-8')
    fid = get_fid(name).encode('utf-8')
    data = {
        'BDUSS':bduss,
        '_client_id':'wappc_1454578461495_469',
        '_client_type':type,
        '_client_version':"7.2.0",
        '_phone_imei':'F8527C479CC9913F5DFE5C38B5E56031',
        'anonymous':'1',
        'content':content,
        'fid':fid,
        'kw':name,
        'tbs':tbs,
        'tid':tid,
        'title':''
    }
    sign = 'BDUSS=%s_client_id=%s_client_type=%s_client_version=%s_phone_imei=%sanonymous=%scontent=%sfid=%skw=%stbs=%stid=%stitle=%s' %(data['BDUSS'], data['_client_id'], data['_client_type'], data['_client_version'], data['_phone_imei'], data['anonymous'], data['content'], data['fid'], data['kw'], data['tbs'], data['tid'], data['title'])
    sign_md5 = hashlib.md5(sign + 'tiebaclient!!!').hexdigest().upper()
    data['sign'] = sign_md5
    #print data
    ADD_URL = 'http://c.tieba.baidu.com/c/c/post/add'
    add_request = requests.post(ADD_URL, data=data)
    status = add_request.text
    return 'Post Add Status %s' %(status)
