# -*- coding: utf-8 -*-
import re
import requests
HEADERS = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT':'1',
    'Host':'tieba.baidu.com',
    'Origin':'http://tieba.baidu.com',
    'Referer':'http://tieba.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
def sign(name, cookies):
    SIGN_URL = 'http://tieba.baidu.com/sign/add'
    tbs = get_tbs(cookies, name)
    data = {
        'ie':'utf-8',
        'kw':name,
        'tbs':tbs
        }
    sign_request = requests.post(SIGN_URL, headers=HEADERS, cookies=cookies, data=data)
    pattern_sign = re.compile(r'"errno":(\d+?),')
    try:
        status = pattern_sign.search(sign_request.text).group(1)
    except:
        status = 'unknown error'
    return 'Sign Status %s' %(status)

def get_tbs(cookies, name):
    TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
    tbs_request = requests.get(TBS_URL, cookies=cookies, headers=HEADERS)
    pattern_tbs = re.compile(r'"tbs":"(.+?)",')
    tbs = pattern_tbs.search(tbs_request.text).group(1)
    return tbs