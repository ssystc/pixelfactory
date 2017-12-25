# coding: utf-8

from taskdata import TaskData
from workflowdata import WorkflowData
from moduledata import ModuleData
from basemodule import Module, StartModule, EndModule, ModuleState
from common.const import ErrorCode
from common import fs, webos, dataserver, tiffserver
from common.error import MsgException
from model.taskstate import TaskState, TaskStateDao
from model.logininfo import LoginInfo, LoginInfoDao
from model.stateclan import StateClan, StateClanDao
from collections import defaultdict
import config
import time
import os
import json
import threading
import traceback
import modulefactory
import shutil
import random
import traceback
from common.userserver import getTokenByuserid
import uuid


class Workflow(object):
    def __init__(self, taskObj, wfObj, userId):
        super(Workflow, self).__init__()
        self.userId = userId
        self.taskData = TaskData(taskObj)
        self.wfData = WorkflowData(wfObj)
        self.modules = {
            Module.START_MODULE_NAME: StartModule(self),
            Module.END_MODULE_NAME: EndModule(self)
        }
        self._pause = False
        self._stop = False
        self._initModules = False
        self.submitTime = time.time()
        self.startTime = None
        self.finishedTime = None

        self.errorCode = 0
        self.errorMsg = ''

        self._taskStateId = None

        # 本地文件系统
        # self._rootDir = os.path.join(config.FILE_SYSTEM_ROOT, self.taskData.id)
        
        self._rootDir = ('%s%s%s') % (config.FILE_SYSTEM_ROOT, self.taskData.id, uuid.uuid4())
        
        # webos上对应的输出目录
        self._outputDirId = None

        self._dirInit = False
        
        self.lastTaskState = None


    def start(self):
        threading.Thread(target=self.run).start()


    def addModule(self, module):
        if module.name in self.modules and module is not self.modules[module.name]:
            return ErrorCode.DuplicateModule

        # for require in module.require:
        #     if require in self.modules:
        #         if require == Module.START_MODULE_NAME:
        #             self.modules[Module.START_MODULE_NAME].addNext(module.name)
        #         reqModule = self.modules[require]
        #         if not module.name in reqModule.next:
        #             return ErrorCode.ConnectModuleError

        # for next in module.next:
        #     if next in self.modules:
        #         if next == Module.END_MODULE_NAME:
        #             self.modules[Module.END_MODULE_NAME].addRequire(module.name)
        #         nextModule = self.modules[next]
        #         if not module.name in nextModule.require:
        #             return ErrorCode.ConnectModuleError

        for require in module.require:
            if require in self.modules:
                self.modules[require].addNext(module.name)
            
        
        for next in module.next:
            if next in self.modules:
                self.modules[next].addRequire(module.name)

        self.modules[module.name] = module
        module.workflow = self
        return ErrorCode.NoError

    def addModules(self, modules, sname):
        for name in modules:
            module = modules[name]
            self.addModule(module)

    def removeModules(self, modules):
        for name in modules:
            if name in self.modules:
                module = self.modules[name]

                # 断开连接
                for req in module.require:
                    if not req in modules and req in self.modules:
                        self.modules[req].next.remove(name)
                for next in module.next:
                    if not next in modules and next in self.modules:
                        self.modules[next].require.remove(name)

                self.modules.pop(name)

    def getModule(self, name):
        return self.modules.get(name)

    @staticmethod
    def iterModules(modules, sname, ename, func):
        def __iterModule(module):
            for nxt in module.next:
                
                if nxt == ename:
                    break
                nmodule = modules.get(nxt)
                
                if nmodule and func(nmodule):
                    __iterModule(nmodule)
        smodule = modules.get(sname)
        
        if smodule:
            __iterModule(smodule)
        else:
            config.Log.info('iter smodule is None')

    def getModules(self, sname, ename):
        modules = {}
        def __iterFunc(module):
            modules[module.name] = module
            return True
        Workflow.iterModules(self.modules, sname, ename, __iterFunc)
        return modules

    def getNextModuleNameByModuleClass(self, moduleName, nextModuleClass):
        nextName = []
        def __iterFunc(module):

            if module.moduleData and module.moduleData.moduleClass == nextModuleClass:
                print module.moduleData
                nextName.append(module.name)
                return False
            return True
        Workflow.iterModules(self.modules, moduleName, None, __iterFunc)
        return nextName[0] if nextName else None

    def getStartModule(self):
        return self.modules.get(Module.START_MODULE_NAME)

    def getEndModule(self):
        return self.modules.get(Module.END_MODULE_NAME)

    def getModuleState(self, name):
        if name in self.modules:
            module = self.modules[name]
            return module.state
        return ModuleState.Unknown

    def canModuleReady(self, name):
        if not name in self.modules:
            return False
        module = self.modules[name]
        for require in module.require:
            if self.getModuleState(require) != ModuleState.Finished:
                return False
        return True

    # 设置前置模块已经完成的模块的状态为Ready
    def _setModuleReady(self, names):
        for name in names:
            if self.canModuleReady(name):
                self.modules[name].state = ModuleState.Ready

    # 执行已经准备好的模块
    def _runReadyModule(self):
        for name, module in self.modules.items():
            if module.canRun():
                config.Log.info('%s run module: %s' % (self.getTaskId(), module))
                module.starttime = time.time()
                module.prepareInputOutput()
                module.run()
                module.state = ModuleState.Runing


    # 检查当前正在执行的模块是否完成
    # 如果完成且没有错误，则修改模块的状态为完成
    # 如果有错误出现，则修改模块状态为错误
    def _checkFinished(self):
        hasComplate = False
        hasError = False
        for name, module in self.modules.items():
                
            if module.state == ModuleState.Runing or module.state == ModuleState.Edit:
                if module.isFinished():
		    
                    module.endtime = time.time()

                    if module.getlltsId() and module.getlltsId() != -2 and module.getlltsId() != -1:
                        stateclan = StateClan(module.getlltsId(), self.getTaskId(), module.stateClan(), self.userId, name, module.starttime, module.endtime)
                        try:
                            StateClanDao.addStateClan(stateclan)
                        except:
                            config.Log.info(u'向stateclan表中添加数据失败')

                    module.onFinished()
                    config.Log.info('%s module finished: %s:%d' % (self.getTaskId(), module, module.exitCode()))

                    if module.hasError():
                        module.state = ModuleState.Error
                        hasError = True
                    else:
                        module.state = ModuleState.Finished
                        self._setModuleReady(module.next)
                    hasComplate = True
        return hasComplate, hasError            

    def _runNext(self):
        self._runReadyModule()
        self.saveWorkflowState()
        
        while True:
            hasComplate, hasError = self._checkFinished()

            if self._stop:
                for name, module in self.modules.items():
                    config.Log.info('name = %s, module = %s, lltsId = %s' % (name, module, module.getlltsId()))
                    module.kill()
                    if module.state == ModuleState.Runing:
                        module.state = ModuleState.Finished
                break

            if hasComplate:
                break
            else:
                time.sleep(1)

    def isFinished(self):
        return self.getEndModule().state == ModuleState.Finished

    def isPause(self):
        return self._pause

    def isStopd(self):
        return self._stop

    def isOver(self):
        return self.isStopd() or self.isFinished() or self.hasError()

    def hasError(self):
        if self.errorCode:
            return True

        for module in self.modules.itervalues():
            if module.state == ModuleState.Error:
                return True

        return False

    def formatError(self):
        errMsg = []
    
        for module in self.modules.itervalues():
            if module.state == ModuleState.Error:
                # exitCode是llts返回的code， returnCode是module返回的code
                errMsg.append('%s %s %s %s' % (module.name, module.exitCode(), module.returnCode(), module.returnMsg()))
                
        if self.errorCode:
            errMsg.append('%s %s %s' % (self.getTaskId(), self.errorCode, self.errorMsg))
            
        return '\n\t--> '.join(errMsg)

    def resetState(self):
        for name, module in self.modules.items():
            module.reset()
        self._stop = False
        self._pause = False
        self._taskStateId = None

        if self._dirInit:
            # shutil.rmtree(self._rootDir)
            self._dirInit = False

    def startRun(self):
        config.Log.info('%s start task: %s' % (self.getTaskId(), self.taskData.id))
        self.startTime = time.time()
        self.resetState()
        self.start()
        return ErrorCode.NoError

    def continueRun(self):
        try:
            config.Log.info('%s continue task: %s' % (self.getTaskId(), self.taskData.id))
            self._pause = False
            self.start()
            return ErrorCode.NoError
        except:
            config.Log.info(traceback.format_exc())

    def stopRun(self):
        config.Log.info('%s stop task: %s' % (self.getTaskId(), self.taskData.id))
        self._stop = True
        return ErrorCode.NoError

    def pauseRun(self):
        config.Log.info('%s pause task %s' % (self.getTaskId(), self.taskData.id))
        self._pause = True
        self.saveWorkflowState()
        return ErrorCode.NoError
    
    def run(self):
        try:
            self.initModules()
            self.prepareFsDir()
        except MsgException, e:
            config.Log.info(traceback.format_exc())
            self.errorCode = e.code
            self.errorMsg = e.msg

        self.saveWorkflowState()
        while True:
            if self.isFinished() or self.hasError():
                err = self.formatError()
                if err:
                    config.Log.info('%s run over \n\t--> %s' % (self.getTaskId(), self.formatError()))
                else:
                    config.Log.info('%s run over sucess' % self.getTaskId())
                break
            try:
                self._runNext()
            except MsgException, e:
                config.Log.info(traceback.format_exc())
                self.errorCode = e.code
                self.errorMsg = e.msg

            if self._stop:
                # self.resetState()
                config.Log.info('%s task stoped' % self.getTaskId())
                break
            if self._pause:
                self.saveWorkflowState()
                config.Log.info('%s task paused' % self.getTaskId())
                break
        
        if self.isOver():
            self.finishedTime = time.time()
            self.saveWorkflowState()

    def getState(self):
        taskId = self.getTaskId()
        userId = self.userId
        
        state = {
            'paused': self._pause,
            'state': 2 if self.isOver() else 1,
            'errorCode': self.errorCode,
            'errorMessage': self.errorMsg,
            'taskId': taskId
        }

        uploading = False

        for name, module in self.modules.items():
            # stateclanUid = uuid.uuid4().hex
            stateclanUid = module.getlltsId()
            # 'detail': module.stateClan(),
            moduleState = {
                'code': module.state,
                'detail': stateclanUid,
                'exitCode': module.exitCode(),
                'returnCode': module.returnCode(),
                'returnMsg': module.returnMsg(),
                'fsid': module.outdirid,
                'uploading': module.uploading
            }
                
            #stateclan = StateClan(stateclanUid, taskId, module.stateClan(), userId, name, module.starttime, module.endtime)
            #try:
            #    StateClanDao.addStateClan(stateclan)
            #except:
            #    config.Log.info(u'向stateclan表中添加数据失败')

            state[name] = moduleState

            if module.uploading:
                uploading = True

        state['fileuploading'] = uploading

        return state

    def initModules(self):
        if self._initModules:
            return

        self._initModules = True
        names = defaultdict(int)
        
        for module in self.wfData.modules:
            md = ModuleData(module)
            require, next, find = self.wfData.getConnectModules(md.flowId)
            if not find:
                continue
            m = modulefactory.createModule(md.moduleClass, md.flowId, require, next, self, md)
            if m:
                if names[md.name] > 0:
                    m.outdirname = '%s%d' % (md.name, names[md.name])
                    
                else:
                    m.outdirname = md.name
                names[md.name] += 1
                err = self.addModule(m)
                config.Log.info('%s add module:%s:%d' % (self.getTaskId(), m, err))

            else:
                config.Log.info('%s create module failed : %s' % (self.getTaskId(), md.flowId))
                
        for mname, module in self.modules.items():
            for nm in module.next:
                if nm not in self.modules:
                    raise MsgException(ErrorCode.ConnectModuleError, u'初始化模块时，模块连接出错')
            for pm in module.require:
                if pm not in self.modules:
                    raise MsgException(ErrorCode.ConnectModuleError, u'初始化模块时，模块连接出错')


    def getModuleInputMap(self, moduleName):
        ret = {}
        for io in self.wfData.iomap:
            try:
                iput = io.get('input')
                if iput['id'] == moduleName:
                    ret[iput['name']] = io['output']
            except KeyError, e:
                config.Log.info('%s %s' % (self.getTaskId(), e))
                config.Log.info('%s %s' % (self.getTaskId(), traceback.format_exc()))
        return ret

    def prepareFsDir(self):
        if self._dirInit:
            return
	
        config.Log.info('start prepareFsDir')
        
        userid = self.userId
        username = LoginInfoDao.queryUsernameByuserid(userid)

        def _createLocalFiles(dirId, fsRoot, createFile = True):
            fs.createDir(fsRoot)
            dirs = webos.listDir(userid, dirId)
		
            config.Log.info(dirs)

            for d in dirs:
                fpath = os.path.join(fsRoot, d['path'])
                if d['type'] == 'dir':
                    _createLocalFiles(d['id'], fpath)
                elif createFile:
                    ft = webos.checkFileType(fpath)
                    if ft == webos.FileType.NORMAL_FILE:
                        dataserver.downloadFile(d['metadataid'], fpath)
                        self.taskData.replaceArgs(d['metadataid'], fpath)
                    elif ft == webos.FileType.TIFF_FILE:
                        url = tiffserver.queryDataUrl(d['metadataid'], userid)
                        if not url:
                            raise MsgException(ErrorCode.GetNetimgUrlFaild, u'get netimg url faild. metadataid = %s' % d['metadataid'])
                        self.taskData.replaceArgs(d['metadataid'], url)

                    else:
                        # TODO url for shp
                        pass
                        
        # 重命名历史输出目录并创建新的输出目录
        try:
            dirs = webos.listDir(userid, self.taskData.rootDir)
            config.Log.info(dirs)
        except:
            config.Log.info(traceback.format_exc())
            config.Log.info('listDir error')
            return ErrorCode.ListDirError

        config.Log.info('prepare list dir: %s' % dirs)

        for d in dirs:
            if d['path'] == config.INPUT_DIR_NAME:
                _createLocalFiles(d['id'], os.path.join(self._rootDir, config.INPUT_DIR_NAME))
            elif d['path'] == config.OUTPUT_DIR_NAME:
                config.Log.info('output fs id: %s' % d['id'])
                pretaskstate = TaskStateDao.queryByFsId(d['id'], self.userId)
                config.Log.info('pretaskstate: %s' % pretaskstate)
                if pretaskstate:
                    webos.rename(userid, d['id'], self.taskData.rootDir, '%s_%s' % ('output', pretaskstate.id))
                    self._outputDirId = fs.prepareOutputDirOnWebos(userid, username, self.taskData.rootDir, self.wfData.obj)
                    # _createLocalFiles(odirid, self.taskData.dirClassify, os.path.join(self._rootDir, 'output'), False)
                else:
                    self._outputDirId = d['id']
                    # _createLocalFiles(d['id'], self.taskData.dirClassify, os.path.join(self._rootDir, 'output'), False)

        if not self._outputDirId:
            self._outputDirId = fs.prepareOutputDirOnWebos(userid, username, self.taskData.rootDir, self.wfData.obj)

        self._dirInit = True
        config.Log.info('download all file')

    def getRootDir(self):
        return self._rootDir

    def getOutputDir(self):
        return os.path.join(self._rootDir, config.OUTPUT_DIR_NAME)

    def getModuleJsonDir(self):
        return os.path.join(self._rootDir, 'flow')

    def getTempDir(self):
        return os.path.join(self._rootDir, 'tmp')

    def getOutputDirId(self):
        return self._outputDirId

    def getTaskId(self):
        return self.taskData.id

    def getStatus(self):
        if self.isStopd():
            return 'Stoped'
        elif self.isFinished():
            return 'Finished'
        elif self.hasError():
            return 'Error'
        else:
            return 'Running'


    def saveWorkflowState(self):
        status = self.getStatus()
        taskstate = TaskState(self.taskData.id, self._pause, self.submitTime, self.startTime, self.finishedTime, self.getState(), self._outputDirId, self.taskData.name, self.taskData.flowId, self.wfData.name, status, self.formatError() if status=='Error' else '', self.userId)
        if self._taskStateId:
            TaskStateDao.modifyTaskState(self._taskStateId, taskstate, self.userId)
        else:
            self._taskStateId = TaskStateDao.addTaskState(taskstate)
        self.lastTaskState = TaskStateDao.lastTaskState(self.taskData.id, self.userId)
        
        




