# coding: utf-8

import time
from basemodule import Module, ModuleState
from common.fs import createDir
from common import llts, lltsconst, webos
from common.const import ErrorCode
from moduledata import ModuleData
from fileupload import FileUpload
import os
import config
import shutil

class LLTSModule(Module):
    
    def __init__(self, name, require, next, workflow, data):
        super(LLTSModule, self).__init__(name, require, next, workflow, data)
        self.lltsId = -2
        self.err = ErrorCode.NoError
    
    def _getFileName(self):
        fileDir = self.workflow.getModuleJsonDir()
        return os.path.join(fileDir, '%s.json' % self.moduleData.flowId)

    def run(self):
        createDir(self.workflow.getModuleJsonDir())
        self.moduleData.tmpDir = os.path.join(self.workflow.getTempDir(), self.outdirname)
        createDir(self.moduleData.tmpDir)
        createDir(os.path.join(self.workflow.getOutputDir(), self.outdirname))

        filename = self._getFileName()
        config.Log.info('write module json to file: %s' % filename)
        self.moduleData.saveToFile(filename)

        self.lltsId = llts.start(self.moduleData.op, self.moduleData.version, filename, self.moduleData.tags)
        config.Log.info('start llts task: %s' % self.lltsId)
        self.err = ErrorCode.NoError
        if not self.lltsId:
            self.err = ErrorCode.LLTSError
    
    def canRun(self):
        if self.state == ModuleState.Ready:
            agentStatistic = llts.getAgentStatistic()
            if agentStatistic['FREE'] > agentStatistic['BUSY']:
                return True
            else:
                return False
        else:
            return False

    
    def kill(self):
        if self.lltsId:
            llts.kill(self.lltsId)


    def isFinished(self):
        if not self.lltsId:
            return True

        if self.lltsId == -2:
            return False
        elif self.lltsId == -1:
            return True

        state = llts.getState(self.lltsId)
        if state[lltsconst.RequestField.STATUS] in [lltsconst.TaskStatus.FINISHED, lltsconst.TaskStatus.ENDED]:
            config.Log.info('llts task exit: %s, state = %s' % (self.lltsId, state[lltsconst.RequestField.STATUS]))
            self.err = state[lltsconst.RequestField.EXIT_CODE]
            return True
        return False

    def exitCode(self):
        return self.err

    def stateClan(self):
        # return {}
        return llts.queryClan(self.lltsId) if self.lltsId else {}

    def getlltsId(self):
        return self.lltsId

    def reset(self):
        super(LLTSModule, self).reset()
        self.kill()
        self.lltsId = -2
        self.err = ErrorCode.NoError

    def onFinished(self):
        filename = self._getFileName()
        with open(filename) as f:
            self.moduleData = ModuleData(file = f)

        # shutil.rmtree(self.moduleData.tmpDir)
        self.uploading = True
        FileUpload.addTask(self)
        
