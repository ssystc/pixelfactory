# coding: utf-8

import json
import config
from common.error import MsgException
from common.const import ErrorCode
import traceback

class ModuleData(object):

    def __init__(self, obj = None, file = None):
        assert obj or file, u'ModuleData InValid argument.'

        if not obj:
            try:
                obj = json.load(file)
            except:
                config.Log.info(traceback.format_exc())
                raise MsgException(ErrorCode.LoadJsonError, u'读取json文件错误')
        
        self.__obj = obj
        config.Log.info('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#####%s' % obj)

    @staticmethod
    def create(data):
        if not data:
            return None
        return data if isinstance(data, ModuleData) else ModuleData(obj = data)

    @property
    def id(self):
        return self.__obj.get('id')
    
    @property
    def flowId(self):
        return self.__obj.get('flow_id')

    @flowId.setter
    def flowId(self, newFlowId):
        self.__obj['flow_id'] = newFlowId

    @property
    def name(self):
        return self.__obj.get('name')

    @property
    def op(self):
        return self.__obj.get('op')

    @property
    def version(self):
        return self.__obj.get('version')

    @property
    def icon(self):
        return self.__obj.get('icon')

    @property
    def desc(self):
        return self.__obj.get('desc')

    @property
    def owner(self):
        return self.__obj.get('owner')

    @property
    def createDate(self):
        return self.__obj.get('createDate')

    @property
    def type(self):
        return self.__obj.get('type')
    
    
    @property
    def isManual(self):
        return self.__obj.get('manual', False)

    @property
    def redirectUrl(self):
        return self.__obj.get('redirect')

    @property
    def moduleClass(self):
        return self.__obj.get('ModuleClass')
    
    @property
    def state_url(self):
        return self.__obj.get('state_url')
    
    @property
    def start_url(self):
        return self.__obj.get('start_url')
    
    @property
    def stop_url(self):
        return self.__obj.get('stop_url')
    
    @property
    def edit_url(self):
        return self.__obj.get('edit_url')

    @property
    def tmpDir(self):
        return self.__obj.get('tmp')

    @tmpDir.setter
    def tmpDir(self, tdir):
        self.__obj['tmp'] = tdir

    @property
    def tags(self):
        return self.__obj.get('tags', None)

    @property
    def outputFiles(self):
        try:
            return self.__obj['Userproperty']['OutputParameter']['OutPutFilePath']
        except:
            return []

    @property
    def inputFiles(self):
        try:
            return self.__obj['Userproperty']['InputParameter']['InputFilePath']
        except:
            return []

    @property
    def inputConfig(self):
        try:
            return self.__obj['Userproperty']['InputParameter']['Configuration']
        except:
            return []

    def __getProgramStatus(self, name):
        try:
            status = self.__obj['Userproperty']['OutputParameter']['ProgramStatus']
            for statu in status:
                if statu['name'] == name:
                    return statu['value']
        except KeyError:
            return None

    @property
    def returnCode(self):
        return self.__getProgramStatus('ReturnCode') or 0

    @property
    def returnMsg(self):
        return self.__getProgramStatus('ReturnAnalyse') or ''

    def __setParamValue(self, name, value, params):
        for param in params:
            if param['name'] == name:
                param['value'] = value

    def __getParamValue(self, name, params, idx):
        for param in params:
            if param['name'] == name and idx == param.get('index'):
                return param['value']
        return None

    def setInputFile(self, name, value):
        self.__setParamValue(name, value, self.inputFiles)

    def setOutputFile(self, name, value):
        self.__setParamValue(name, value, self.outputFiles)

    def addInputFiles(self, inputs):
        self.inputFiles.extend(inputs)

    def addAllInputToOutput(self):
        self.outputFiles.extend(self.inputFiles)

    def getInputFile(self, name):
        return self.__getParamValue(name, self.inputFiles, None)

    def getOutputFile(self, name, idx = None):
        return self.__getParamValue(name, self.outputFiles, idx)

    def getMultiOutputs(self, name):
        return [o for o in self.outputFiles if o['name'] == name]

    def setMultiInputs(self, inputs):
        if not inputs:
            return
        name = inputs[0]['name']
        for ipt in self.inputFiles:
            if ipt['name'] == name:
                self.inputFiles.remove(ipt)
                break
        self.addInputFiles(inputs)

    def reset(self):
        def __reset(params):
            name2Obj = {}
            for inp in params:
                name2Obj[inp['name']] = inp
            del params[:]
            for inp in name2Obj.itervalues():
                if inp.get('multi'):
                    inp.pop('index')
                params.append(inp)
        __reset(self.inputFiles)
        __reset(self.outputFiles)

    def saveToFile(self, filename):
        with open(filename, 'w') as f:
            try:
                json.dump(self.__obj, f, ensure_ascii=False)
            except:
                raise MsgException(ErrorCode.WriteModuleJsonError, 'write flow file error: %s' % traceback.format_exc())
