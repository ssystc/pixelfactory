# coding: utf-8

from threading import Thread
from Queue import Queue, Empty
import multiprocessing
import time
import os
import traceback
from model.logininfo import LoginInfoDao, LoginInfo
import config
from common import webos
from common.userserver import getTokenByuserid
from common.dataserver import uploadModuleJson
import json


class FileUpload(Thread):

    __instance = []
    taskQueue = Queue()

    @classmethod
    def addTask(cls, module):
        def taskFunc():
            try:
                status = False

                fsRoot = os.path.join(module.workflow.getOutputDir(), module.outdirname)

                userid = module.workflow.userId

                outdirid = module.workflow.getOutputDirId()
                config.Log.info('begin upload: %s' % fsRoot)
                module.outdirid = webos.uploadDir(userid, outdirid, fsRoot)
                module.workflow.saveWorkflowState()
                status = True
                config.Log.info('end upload: %s' % fsRoot)
            except:
                config.Log.info(traceback.format_exc())
                config.Log.info('upload task error: %s' % fsRoot)
            finally:
                module.uploading = False
                # state = False
                # i = 0
                # for m in module.workflow.modules:
                #     if hasattr(m, 'uploading'):
                #         if m.uploading:
                #             i = i+1
                # if i == 0 and (module.workflow.isFinished() or module.workflow.hasError()):
                #     state = True
                # try:
                #     taskId = module.workflow.getTaskId()
                #     folderId = module.workflow._outputDirId,
                #     jsonFileDir = module._getFileName()
                #     status = uploadModuleJson(taskId, folderId, jsonFileDir, userid, state)
                #     if status != 'true':
                #         config.Log.info('upload modulejson failed, jsonFileDir = %s' % jsonFileDir)
                # except:
                #     config.Log.info('upload modulejson failed, jsonFileDir = %s' % jsonFileDir)
        cls.taskQueue.put(taskFunc)

    @classmethod
    def startThread(cls, threadNum = 1):
        for i in range(threadNum):
            t = FileUpload()
            t.start()
            cls.__instance.append(t)

    @classmethod
    def stopThread(cls):
        for t in cls.__instance:
            t.stop = True
        cls.__instance = []

    def __init__(self):
        super(FileUpload, self).__init__()
        self.stop = False
        

    def run(self):
        while not self.stop:
            try:
                task = FileUpload.taskQueue.get(timeout=0.5)
                # p = multiprocessing.Process(target=task)
                # p.start()
                # p.join()
                task()
            except Empty:
                pass


