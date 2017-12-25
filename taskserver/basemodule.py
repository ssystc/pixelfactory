# coding: utf-8

from moduledata import ModuleData
from common.const import ErrorCode
from common.error import MsgException
import config
import os
import copy
import traceback


class ModuleState(object):
    Unknown = -1
    Waiting = 0
    Ready = 1
    Runing = 2
    Finished = 3
    Error = 4
    Edit = 5
    Stoped = 6


class Module(object):

    START_MODULE_NAME = '__start_module__'
    END_MODULE_NAME = '__end_module__'

    def __init__(self, name, require, next, workflow, data = None):
        def getArray(v):
            if v:
                return v if isinstance(v, list) else [v]
            return None

        self.name = name
        self.require = getArray(require) or [Module.START_MODULE_NAME]
        self.next = getArray(next) or [Module.END_MODULE_NAME]
        self.workflow = workflow
        self.moduleData = ModuleData.create(data)
        self.state = ModuleState.Waiting
        self.index = None
        self.finished = False
        self.inputMap = workflow.getModuleInputMap(name) if workflow else {}
        self.outdirname = None
        self.outdirid = None
        self.uploading = False
        self.starttime = None
        self.endtime = None

    def __repr__(self):
        return '<taskid:%s, name:%s, require:%s, next:%s, finished:%d, exitCode:%d, returnCode:%d, returnMsg:%s, uploading:%s>' \
            % (self.workflow.getTaskId(), self.name, self.require, self.next, 
            self.isFinished(), self.exitCode(), self.returnCode(), self.returnMsg(), self.uploading)

    def run(self):
        self.finished = True
    
    def canRun(self):
        return self.state == ModuleState.Ready
    
    def isFinished(self):
        return self.finished

    def exitCode(self):
        return ErrorCode.NoError

    def returnCode(self):
        return self.moduleData.returnCode if self.moduleData else 0

    def hasError(self):
        return self.exitCode() or self.returnCode()

    def returnMsg(self):
        return self.moduleData.returnMsg if self.moduleData else ''

    def addNext(self, moduleName):
        if not moduleName in self.next:
            self.next.append(moduleName)

    def addRequire(self, moduleName):
        if not moduleName in self.require:
            self.require.append(moduleName)

    def kill(self):
        pass

    def stateClan(self):
        pass
    
    def getlltsId(self):
        pass

    def reset(self):
        self.state = ModuleState.Waiting
        self.moduleData.reset()

    def getType(self):
        return self.moduleData.type

    def _getOutput(self, outputName, idx = None):
        for opt in self.moduleData.outputFiles:
            if opt['name'] == outputName and (opt.get('index') == idx or not opt.get('multi', False)):
                return opt['value']

    def _getOutputs(self, outputName):
        ret = []
        for opt in self.moduleData.outputFiles:
            if opt['name'] == outputName:
                ret.append(opt)
        return ret

    def _getInputValueFromInputMap(self, inputName, idx = None):
        if inputName in self.inputMap:
            opt = self.inputMap[inputName]
            oname = opt['id'] or Module.START_MODULE_NAME
            omodule = self.workflow.getModule(oname)
            ovalue = omodule._getOutput(opt['name'], idx)
            return ovalue

    def _getInputsFromInputMap(self, inputName):
        if inputName in self.inputMap:
            opt = self.inputMap[inputName]
            oname = opt['id'] or Module.START_MODULE_NAME
            omodule = self.workflow.getModule(oname)
            return copy.deepcopy(omodule._getOutputs(opt['name']))
        else:
            config.Log.info('inputs is None')
            return []

    def _prepareInput(self):
        multis = []

        try:
            for inputfile in self.moduleData.inputFiles:
                if inputfile.get('multi', False):
                    multis.append(inputfile['name'])
                else:
                    inputfile['value'] = self._getInputValueFromInputMap(inputfile['name'], self.index)

            for multi in multis:
                inputs = self._getInputsFromInputMap(multi)
                if inputs:
                    for inp in inputs:
                        inp['name'] = multi
                    self.moduleData.setMultiInputs(inputs)
        except:
            config.Log.info(traceback.format_exc())
            raise MsgException(ErrorCode.PrepareInputsError, u'prepare inputs error.')

    def _prepareOutput(self):

        def __getBaseName():
            for inp in self.moduleData.inputFiles:
                if inp.get('value') and os.path.exists(inp.get('value')):
                    return inp.get('value')
            return self.name

        try:
            basefile = __getBaseName()
            if basefile:
                basename = os.path.splitext(os.path.basename(basefile))[0]
                outputDir = os.path.join(self.workflow.getOutputDir(), self.outdirname)
                for outputfile in self.moduleData.outputFiles:
                    outputfile['value'] = os.path.join(outputDir, basename + outputfile['suffix'])
        except:
            config.Log.info(traceback.format_exc())
            raise MsgException(ErrorCode.PrepareOutputsError, u'prepare outputs error.')

    # 实现了基本的输入输出设置功能，子类可重写方法，实现高级功能
    def prepareInputOutput(self):
        self._prepareInput()
        self._prepareOutput()


    # 执行完成后的回调
    def onFinished(self):
        pass


class EndpointModule(Module):
    def __init__(self, name, wf):
        self.name = name
        self.require = []
        self.next = []
        self.workflow = wf
        self.moduleData = None
        self.state = None
        self.finished = False
        self.outdirname = None
        self.outdirid = None
        self.uploading = False	
        self.starttime = None
        self.endtime = None
    

    def isFinished(self):
        return self.finished

class StartModule(EndpointModule):
    def __init__(self, wf):
        super(StartModule, self).__init__(Module.START_MODULE_NAME, wf)
        with open('./taskserver/static/StartModuleConfig.json') as f:
            self.moduleData = ModuleData(file = f)

    def reset(self):
        self.state = ModuleState.Ready

    # 根据输入根目录设置起始模块的输出
    def prepareInputOutput(self):
        rootDir = self.workflow.getRootDir()
        for i in range(3):
            self.moduleData.setOutputFile(config.AUTO_DIRS[0], os.path.join(rootDir, config.INPUT_DIR_NAME, config.INPUT_DIRS[0]))
        self.finished = True
        # 任务参数添加到输入文件
        self.moduleData.addInputFiles(self.workflow.taskData.args)
        # 将输入全部拷贝到输出
        self.moduleData.addAllInputToOutput()

class EndModule(EndpointModule):
    def __init__(self, wf):
        super(EndModule, self).__init__(Module.END_MODULE_NAME, wf)

    def reset(self):
        self.state = ModuleState.Waiting

    def prepareInputOutput(self):
        pass
