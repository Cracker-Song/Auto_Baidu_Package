# -*- coding: utf-8 -*-
import re
import requests
import Robot


def get_atme(cookies):
    atme_url = 'http://tieba.baidu.com/i/yoururl/atme'
    atme_request = requests.get(atme_url, cookies=cookies)
    atme_content = atme_request.text
    atme_pattern = re.compile(r'<div class="atme_text clearfix j_atme">\s+(.+?)\s+(.+?)\s+</div>')
    atme_user_pattern = re.compile(r'<div class="atme_user">.*?target="_blank">(.*?)</a></div>')
    atme_content_pattern = re.compile(r'<div class="atme_content">.*?target="_blank">(.*?)</a></div>')
    #atme_time_pattern = re.compile(r'<div class="feed_time">(\d+)-(\d+) (\d+):(\d+)</div>')
    atme_keyword_pattern = re.compile(r'召唤逗比')
    atme_url_pattern = re.compile(r'href="/p/(\d+)')
    atme_url_all_pattern = re.compile(r'<a href="(.+?)" target="_blank">')
    atme_names_pattern = re.compile(r'<a class="itb_kw" href=".+?target="_blank">.+?</a>')
    atme_name_unicode_pattern = re.compile(r'href="/f\?kw=(.+?)"')
    atme_name_pattern = re.compile(r'target="_blank">(.+?)</a>')
    atmes = atme_pattern.findall(atme_content)
    names = atme_names_pattern.findall(atme_content)

    post = []
    last_urls = []
    post_log = open('./last_post.log', 'r')
    for urls in post_log.readlines():
        last_urls.append(urls[:-1])
    post_log.close()
    #print last_urls
    count = 0
    for atme in atmes:
        #print type(atme[1].encode('utf-8'))
        #print atme[1].encode('utf-8')
        #print atme
        name_unicode = atme_name_unicode_pattern.search(names[count]).group(1)
        name = atme_name_pattern.search(names[count]).group(1)[:-1]
        #print name
        count += 1
        url_all = atme_url_all_pattern.search(atme[0]).group(1)
        #print url_all
        #print last_urls
        if atme_keyword_pattern.search(atme[1].encode('utf-8')) and url_all not in last_urls:
            tmp_url = atme_url_pattern.search(atme[1]).group(1)
            tmp_user = atme_user_pattern.search(atme[0]).group(1)[:-1]
            tmp_content = atme_content_pattern.search(atme[1]).group(1)
            tmp_new_content = tmp_content.replace(u'<b>@yourname</b> \u53ec\u5524\u9017\u6bd4 ', '')
            tmp_respond = Robot.robot(tmp_new_content, tmp_user)
            user = tmp_user
            urls_all = url_all
            #print urls_all
            respond = tmp_respond
            urls = tmp_url
            user_and_content = [user, urls_all, respond, urls, name, name_unicode]
            post.append(user_and_content)
    return post
