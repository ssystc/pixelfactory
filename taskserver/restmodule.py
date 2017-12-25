# coding: utf-8

from basemodule import Module, ModuleState
from common.fs import createDir
from common import llts, lltsconst, webos
from common.const import ErrorCode
from moduledata import ModuleData
from fileupload import FileUpload
import os
import config
import shutil
import requests
import time
import json
from model.taskstate import TaskStateDao
from common.error import MsgException


class RestModule(Module):
    def __init__(self, name, require, next, workflow, data):
        super(RestModule, self).__init__(name, require, next, workflow, data)
        self.restmoduleId = -2
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
        
        num = len(self.require)
        
        # while True:
        #     i = 0
        #     for require in self.require:
        #         if self.workflow.modules[require].uploading == False:
        #             i = i+1
        #     if i == num:
        #         break
        #     else:
        #         time.sleep(5)
        
        try:
            rep = requests.post(self.moduleData.start_url,data={
                'module_info': filename
            })
            startcontent = json.loads(rep.content)
            config.Log.info(rep.content)
            self.restmoduleId = startcontent['instance_id']
            config.Log.info('start restmodule %s' % self.restmoduleId)
        except:
            self.error = ErrorCode.StartRestModuleError
            raise MsgException(ErrorCode.StartRestModuleError, u'start restmodule error')
            
        self.err = ErrorCode.NoError

    
    def kill(self):
        try:
            requests.post(self.moduleData.stop_url, data={
                'instance_id': self.restmoduleId
            })
        except:
            config.Log.info('can not kill restmodule')
    
    def isFinished(self):
        if not self.restmoduleId:
            return True
        
        if self.restmoduleId == -2:
            return False
        
        rep = requests.get('%s%s%s' % (self.moduleData.state_url, '/', self.restmoduleId))
        state = json.loads(rep.content)
        #state['stateclan'], state['status'], state['exitcode']
        
        if state['status'] == 'wait_edit':
            self.state = ModuleState.Edit
            lasttaskstate = self.workflow.lastTaskState
            clan = json.loads(lasttaskstate.clan)
            modulestatus = clan[self.name]['code']
            if modulestatus != ModuleState.Edit:
                self.workflow.saveWorkflowState()
            
            
        if state['status'] == 'run':
            self.state = ModuleState.Runing
            lasttaskstate = self.workflow.lastTaskState
            clan = json.loads(lasttaskstate.clan)
            modulestatus = clan[self.name]['code']
            if modulestatus != ModuleState.Runing:
                self.workflow.saveWorkflowState()
        
        if state['status'] in ['end', 'wrong']:
            config.Log.info('restmodule exit: %s, state = %s' % (self.restmoduleId, state['status']))
            self.err = state['exitcode']
            return True
        return False
    
    def exitCode(self):
        return self.err
    
    def getlltsId(self):
        return self.restmoduleId
    
    def stateClan(self):
        # return {}
        try:
            rep = requests.get('%s%s%s' % (self.moduleData.state_url, '/', self.restmoduleId))
            content = json.loads(rep.content)
            return content['stateclan']
        except:
            return {}
    
    
    def reset(self):
        super(RestModule, self).reset()
        self.kill()
        self.lltsId = -2
        self.err = ErrorCode.NoError
    
    def onFinished(self):
        filename = self._getFileName()
        with open(filename) as f:
            self.moduleData = ModuleData(file=f)
        
        # shutil.rmtree(self.moduleData.tmpDir)
        self.uploading = True
        FileUpload.addTask(self)