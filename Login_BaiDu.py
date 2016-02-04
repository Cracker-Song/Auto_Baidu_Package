# -*- coding: utf-8 -*-
import re
#import rsa
#import base64
import requests
import pytesseract
from PIL import Image
from StringIO import StringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

POST_URL = 'http://tieba.baidu.com/f/commit/thread/add'
HEADERS = {
    'Host': 'passport.baidu.com',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
def get_init_cookies():
    INIT_URL = 'https://passport.baidu.com/passApi/html/_blank.html'
    init_request = requests.get(INIT_URL, headers=HEADERS)
    return init_request.cookies

def get_token(cookies):
    TOKEN_URL = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&logintype=dialogLogin'
    token_data = requests.get(TOKEN_URL, headers=HEADERS, cookies=cookies)
    pattern = re.compile('"token" : "(.+?)"')
    token = pattern.search(token_data.text).group(1)
    return token

def get_key(token, cookies):
    PUBLICKEY_URL = 'https://passport.baidu.com/v2/getpublickey?token=%s' %(token)
    publickey_request = requests.get(PUBLICKEY_URL, headers=HEADERS, cookies=cookies)
    publickey_data = publickey_request.text
    pattern_rsakey = re.compile('"key":\'(.*?)\'')
    target_rsakey = pattern_rsakey.search(publickey_data).group(1)
    pattern_publickey = re.compile(r'"pubkey":\'(.*?)\\n\'')
    target_key = pattern_publickey.search(publickey_data).group(1)
    enter='''
'''
    target_key = target_key.replace('\\n', enter)
    keys = {'rsakey':target_rsakey, 'publickey':target_key}
    #print keys
    return keys

def get_cookies(USERNAME, PASSWORD):
    LOGIN_URL = 'https://passport.baidu.com/v2/api/?login'

    raw_cookies = get_init_cookies()
    token = get_token(raw_cookies).encode('utf-8')
    keys=get_key(token,raw_cookies)
    publickey = keys['publickey']
    rsakey = keys['rsakey'].encode('utf-8')
    #publickey_rsa = rsa.PublicKey.load_pkcs1_openssl_pem(publickey)
    #password = rsa.encrypt(PASSWORD, publickey_rsa)
    #password = base64.b64encode(password)
    password = PASSWORD#不需要进行rsa加密,百度js会进行处理
    data = {
        'token':token,
        'username':USERNAME,
        'password':password,
        'rsakey':rsakey,
        'isPhone':'false',
        'staticpage':'http://tieba.baidu.com/tb/static-common/html/pass/v3Jump.html',
        'charset':'GBK',
        'apiver':'v3',
        'u':'http://tieba.baidu.com/#',
        'logintype':'dialogLogin',
        'logLoginType':'pc_loginDialog'
    }
    while True:
        login_request = requests.post(LOGIN_URL, headers=HEADERS, data=data, cookies=raw_cookies)
        pattern_identify_code = re.compile(r'&codeString=(.*?)&userName')
        identify_code = pattern_identify_code.search(login_request.content).group(1)
        identfy_url = 'https://passport.baidu.com/cgi-bin/genimage?%s' %(identify_code)
        identify_image_bineray = requests.get(identfy_url, cookies=raw_cookies)
        try:
            identify_image = Image.open(StringIO(identify_image_bineray.content))
            vcode = pytesseract.image_to_string(identify_image)
            check_vcode_url = 'https://passport.baidu.com/v2/?checkvcode&token=%s&tpl=tb&apiver=v3&verifycode=%s&codestring=%s' %(token, vcode, identify_code)
            check_vcode_result = requests.get(check_vcode_url, headers=HEADERS, cookies=raw_cookies)
            pattern_check_vcode_err = re.compile('"errInfo":{ "no": "(.+?)"')
        except:
            pass
        try:
            check_vcode_err = pattern_check_vcode_err.search(check_vcode_result.content).group(1)
        except:
            check_vcode_err = '0'
            vcode = ''
            #print check_vcode_err
        if check_vcode_err=='0':
            break
    #print vcode
    #print check_vcode_err
    login_data = {
        'token':token,
        'codestring':identify_code,
        'username':USERNAME,
        'password':password,
        'verifycode':vcode,
        'gid':'817FB75-6D73-4900-9A89-4DC12B10690E',
        'rsakey':rsakey,
        'isPhone':'false',
        'staticpage':'http://tieba.baidu.com/tb/static-common/html/pass/v3Jump.html',
        'charset':'GBK',
        'apiver':'v3',
        'u':'http://tieba.baidu.com/#',
        'logintype':'dialogLogin',
        'logLoginType':'pc_loginDialog'
    }
    login = requests.post(LOGIN_URL, headers=HEADERS, cookies=raw_cookies, data=login_data)
    pattern_status = re.compile(r'"err_no=(\d+?)&')
    status = pattern_status.search(login.text).group(1)
    #print login.tex
    log = open('./AutoRun.log','a')
    log.write('Login Status %s\n' %(status))
    log.close()
    #print 'Login Status %s' %(status)
    return login.cookies
#暂不支持手机号,原因不明
#print get_cookies('', '')