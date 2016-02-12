# -*- coding: utf-8 -*-
import AutoRun
import time
log_time = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
log_file = open('./AutoRun.log','a')
log_file.write('%s  Time: %s \n' % (AutoRun.post_add(‘发贴吧名’, ‘帖子tid’, ‘内容‘), log_time))
log_file.close()