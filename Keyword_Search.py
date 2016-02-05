# -*- coding: utf-8 -*-
import re
import requests


def get_tids(name, keyword, content):
    tids = []
    keyword_pattern = re.compile(keyword)
    mark_pattern = re.compile(r'---marked by robot')
    page_url = 'http://tieba.baidu.com/f?kw=%s&ie=utf-8&pn=0' %(name)
    page_request = requests.get(page_url)
    hrefs_pattern = re.compile(r'<a href="/p/(\d+?)"')
    hrefs = hrefs_pattern.findall(page_request.text)
    tid_pattern = re.compile(r'(\d+)')
    count = 0
    for href in hrefs:
        count += 1
        tid_tmp = tid_pattern.search(href).group(1)
        url_tmp = 'http://tieba.baidu.com/p/%s' %(tid_tmp)
        url_request = requests.get(url_tmp)
        tmp_html = url_request.text.encode('utf-8')
        iskeyword = keyword_pattern.search(tmp_html)
        ismarked = mark_pattern.search(tmp_html)
        if iskeyword and not ismarked:
            tids.append(tid_tmp)
        if count>=15:
            break
    return tids