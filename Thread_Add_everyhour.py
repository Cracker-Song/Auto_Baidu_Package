# -*- coding: utf-8 -*-
import AutoRun
import time
log_time = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
log_file = open('./AutoRun.log','a')
log_file.write('%s  Time: %s \n' %(AutoRun.thread_add(‘发贴吧名’, ‘标题’, ‘一楼内容— from Server cloud'),log_time))
log_file.close()