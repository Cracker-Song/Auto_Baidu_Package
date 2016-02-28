# -*- coding: utf-8 -*-
import time
import Auto_Sign
import Post_Add
import Thread_Add
import Keyword_Search
import Keyword_weather
import Get_Atme


try:
    bduss_log = open('./cookies.log', 'r')
    bduss = bduss_log.read()
    bduss_log.close()
    cookies = {
        'BDUSS':bduss
    }
except:
    log = open('./AutoRun.log','a')
    log.write('Login Status %s\n' %('read cookies file error'))
    log.close()


def post_add(name, tid, content):
    return Post_Add.add(cookies, name, tid, content, cookies['BDUSS'], '3')


def thread_add(name, title, content):
    return Thread_Add.add(cookies, name, title, content)


def sign(name):
    return Auto_Sign.sign(name, cookies, cookies['BDUSS'])


def post_with_keyword(name, keyword, content, mark):
    content += mark
    status = []
    for tid in Keyword_Search.get_tids(name, keyword, content):
        status.append(Post_Add.add(cookies, name, tid, content))
        time.sleep(5)
    return status


def post_keyword_weather(name):
    return Keyword_weather.post_weather_tids(name, cookies)


def get_atme():
    return Get_Atme.get_atme(cookies)
