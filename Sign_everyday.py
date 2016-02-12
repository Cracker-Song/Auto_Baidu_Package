# -*- coding: utf-8 -*-
import AutoRun
import time
log_time = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
log_file = open('./AutoRun.log','a')
log_file.write('%s  Time: %s' %(AutoRun.sign(‘签到吧名’),log_time))
log_file.write('\n')

log_file.write('%s  Time: %s' %(AutoRun.sign('签到吧名'),log_time))
log_file.write('\n')
#可添加更多
log_file.close()