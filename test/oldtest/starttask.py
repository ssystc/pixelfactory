# coding: utf-8

import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

host = 'http://localhost:8283'

def _taskop(tid, op, log):
    print u'%s: %s' % (log, tid)
    rep = requests.post("%s%s" % (host, '/api/task/%s' % op), data=[
        ('id', tid)
    ])
    print rep.content

def start(tid):
    _taskop(tid, 'start', u'启动任务')

def stop(tid):
    _taskop(tid, 'stop', u'停止任务')

def pause(tid):
    _taskop(tid, 'pause', u'暂停任务')

def cont(tid):
    _taskop(tid, 'contine', u'继续任务')

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print u'缺少任务id'
        sys.exit(-1)

    taskId = sys.argv[1]
    op = 'start'
    if len(sys.argv) >= 3:
        op = sys.argv[2]

    opfuncs = {
        'start': start,
        'stop': stop,
        'pause': pause,
        'countine': cont,
        'cont': cont
    }

    if op in opfuncs:
        opfuncs[op](taskId)
    else:
        print u'未知操作:%s' % op


