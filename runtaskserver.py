# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from common import zmqutil

from common.const import TaskMessageField, TaskRequestType, ErrorCode
from taskserver.taskmgr import TaskMgr
from taskserver.log import Log, InitLogging
from taskserver.fileupload import FileUpload
from common import fs
import config
import signal
import zmq

# 注册log模块
config.Log = Log

serverStoped = False

def startTask(msg):
    return TaskMgr.startTask(msg)

def pauseTask(msg):
    return TaskMgr.pauseTask(msg)

def continueTask(msg):
    return TaskMgr.continueTask(msg)

def stopTask(msg):
    return TaskMgr.stopTask(msg)

def Terminate(sig, extra):
    global serverStoped
    serverStoped = True
    FileUpload.stopThread()
    Log.info('signaled by %d', sig)

signal.signal(signal.SIGINT, Terminate)
signal.signal(signal.SIGTERM, Terminate)


if __name__ == '__main__':
    Log.info(u'start taskserver...')

    FileUpload.startThread(12)

    try:
        sock = zmqutil.CreateRep()
    except:
        Log.error(u'create socket error!')
        sys.exit(-1)

    opfun = {
        TaskRequestType.StartTask: startTask,
        TaskRequestType.StopTask: stopTask,
        TaskRequestType.PauseTask: pauseTask,
        TaskRequestType.ContinueTask: continueTask
    }

    while not serverStoped:
        try:
            msg = zmqutil.RecvMsg(sock)
        except zmq.error.Again:
            continue

        try:
            if msg[TaskMessageField.Type] in opfun:
                Log.info(u'recv msg: %s', msg)
                ret = opfun[msg[TaskMessageField.Type]](msg)
                zmqutil.SendMsg(sock, ret)
            else:
                Log.error(u'recv unknow msg: %s', msg)
                zmqutil.SendMsg(sock, {
                    TaskMessageField.Type: TaskRequestType.UnKnown,
                    TaskMessageField.ErrCode: ErrorCode.UnknowOption})
        except KeyError, e:
            Log.error(u'recv unknow msg: %s', msg)
            zmqutil.SendMsg(sock, {
                TaskMessageField.Type: TaskRequestType.UnKnown,
                TaskMessageField.ErrCode: ErrorCode.UnknowOption})

    Log.info(u'taskserver stoped')
