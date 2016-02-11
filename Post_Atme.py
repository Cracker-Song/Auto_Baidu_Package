# -*- coding: utf-8 -*-
#import re
import time
import AutoRun


atmes = AutoRun.get_atme()
if atmes:
    post_log = open('./last_post.log', 'a')
    for atme in atmes:
        #print atme
        robot_log = open('./Robot.log', 'a')
        post_content = '@%s %s' % (atme[0], atme[2])
        #print post_content
        #print atme[4]
        #print atme[4]
        status = AutoRun.post_add(atme[4], atme[3], post_content)
        robot_log.write('%s\n' % status)
        #print type(atmes[0][1])
        time.sleep(3)
        post_log.writelines('%s\n' %atme[1])
    robot_log.close()
    post_log.close()
