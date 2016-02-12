# -*- coding: utf-8 -*-
import Login_Baidu as login
cookies = login.get_cookies('你的邮箱账号', '密码')
cookies_file_write = open('./cookies.log', 'w')
cookies_file_write.write(cookies['BDUSS'])
cookies_file_write.close()