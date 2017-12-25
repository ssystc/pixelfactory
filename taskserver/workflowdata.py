# coding: utf-8

class WorkflowData(object):
    
    def __init__(self, obj):
        assert obj, u'WorkflowData InValid argument.'
        self.__obj = obj
    
    @property
    def id(self):
        return self.__obj.get('id')

    @property
    def name(self):
        return self.__obj.get('name')

    @property
    def icon(self):
        return self.__obj.get('icon')

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
    def runMethod(self):
        return self.__obj.get('runMethod')

    @property
    def version(self):
        return self.__obj.get('version')

    @property
    def workflows(self):
        return self.__obj.get('workflow')

    @property
    def iomap(self):
        return self.__obj.get('IOMap')

    @property
    def modules(self):
        return self.__obj.get('modules')

    @property
    def obj(self):
        return self.__obj

    def getConnectModules(self, moduleName):
        wfs = self.workflows
        for wf in wfs:
            if wf.get('flow_id') == moduleName:
                return wf.get('pre_id'), wf.get('next_id'), True
        return None, None, False