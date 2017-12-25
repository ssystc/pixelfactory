# coding: utf-8

import config

class TaskData(object):

    def __init__(self, obj):
        assert obj, u'TaskData InValid argument.'
        self.__obj = obj

    @property
    def id(self):
        return self.__obj.get('id')
    
    @property
    def name(self):
        return self.__obj.get('name')
    
    @property
    def flowId(self):
        return self.__obj.get('flowId')

    @property
    def rootDir(self):
        return self.__obj.get('dir')

    @property
    def dirClassify(self):
        return self.__obj.get('dirclassify')

    @property
    def args(self):
        return self.__obj.get('args', [])

    def replaceArgs(self, old, new):
        for arg in self.args:
            if arg.get('value') == old:
                arg['value'] = new
		
