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
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}
def add(cookies, name, title, content):
    tbs = get_tbs(cookies, name).encode('utf-8')
    fid = get_fid(name).encode('utf-8')
    #print cookies
    data = {
        'ie':'utf-8',
        'kw':name,
        'fid':fid,
        'tbs':tbs,
        'title':title,
        'content':content,
        'tid':'0',
        'floor_num':'0',
        'rich_text':'1',
        '__type__':'thread'
    }
    #print data
    ADD_URL = 'http://tieba.baidu.com/f/commit/thread/add'
    add_request = requests.post(ADD_URL, cookies=cookies, data=data, headers=HEADERS)
    pattern_status = re.compile('err_code":(\d+),')
    try:
        status = pattern_status.search(add_request.text).group(1)
    except:
        status = 'unkown error'
    #print add_request.text
    return 'Add Status %s' %(status)
    #return add_request.text

def get_tbs(cookies, name):
    TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
    tbs_request = requests.get(TBS_URL, cookies=cookies, headers=HEADERS)
    pattern_tbs = re.compile(r'"tbs":"(.+?)",')
    tbs = pattern_tbs.search(tbs_request.text).group(1)
    return tbs

def get_fid(name):
    FID_URL = 'http://tieba.baidu.com/f?ie=utf-8&kw=%s&fr=search' %(name)
    fid_request = requests.get(FID_URL, headers=HEADERS)
    pattern_fid = re.compile(r'PageData.forum = {\s*\'id\': (.+?),')
    fid = pattern_fid.search(fid_request.text).group(1)
    return fid