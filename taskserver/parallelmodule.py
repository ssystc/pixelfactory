# coding: utf-8

from basemodule import Module
from collections import defaultdict
import config
from config import PARALLEL_TEMPLATE as template
import modulefactory
import copy

class ParallelStartModule(Module):
            
    def __init__(self, name, require, next, workflow, data):
        super(ParallelStartModule, self).__init__(name, require, next, workflow, data)
        self.modulesbak = None
        self.modulesGroup = None
        self.mergeName = None

    def __disconnect(self):
        pass
        # self.next = []
        # if self.mergeName:
        #     self.workflow.getModule(self.mergeName).require = []

    def __prepareParallel(self, count):

        if Module.END_MODULE_NAME in self.next:
            config.Log.info('parallel next is end.')
            return

        self.mergeName = self.workflow.getNextModuleNameByModuleClass(self.name, 'merge')

        config.Log.info('mergeName: %s' % self.mergeName)
        # 设置mergemodule中合并数量
        if self.mergeName:
            mergeModule = self.workflow.getModule(self.mergeName)
            mergeModule.setMergeCount(count)

        modules = self.workflow.getModules(self.name, self.mergeName)
        if Module.END_MODULE_NAME in modules:
            modules.pop(Module.END_MODULE_NAME)
        self.modulebak = modules
        self.workflow.removeModules(modules)

        self.__disconnect()

        # 拷贝流程，并加入workflow
        def __copyModules(modules, index):
            newModules = {}
            for name, module in modules.iteritems():
                md = copy.deepcopy(module.moduleData)
                md.flowId = template % (md.flowId, index)
                nname = template % (name, index)
                nrequire = [template % (r, index) if r != self.name else r for r in module.require]
                nnext = [template % (n, index) if n != self.mergeName and n != Module.END_MODULE_NAME else n for n in module.next]
                nmodule = modulefactory.createModule(md.moduleClass, nname, nrequire, nnext, self.workflow, md)
                nmodule.index = index
                nmodule.outdirname = '%s-%d' % (module.outdirname, index)
                
                # 设置输入映射
                for vname, oout in module.inputMap.iteritems():
                    nout = {
                        'id': template % (oout['id'], index) if oout['id'] in modules else oout['id'],
                        'name': oout['name']
                    }
                    nmodule.inputMap[vname] = nout

                newModules[nname] = nmodule
                if self.name in nrequire:
                    self.next.append(nname)
            return newModules

        self.modulesGroup = []
        for i in range(count):
            nmodules = __copyModules(modules, i)
            self.workflow.addModules(nmodules, self.name)
            self.modulesGroup.append(nmodules)

    def prepareInputOutput(self):
        if not self.moduleData.inputFiles:
            inps = [{
                'multi': True,
                'name': inp,
                'value': '',
                'title': '',
                'type': 'url'
            } for inp in self.inputMap]
            self.moduleData.addInputFiles(inps)

        self._prepareInput()
        self.moduleData.addAllInputToOutput()
        inputCounts = defaultdict(int)
        for inp in self.moduleData.inputFiles:
            inputCounts[inp['name']] += 1
        count = max(inputCounts.itervalues())
        self.__prepareParallel(count)

    def reset(self):
        self.__disconnect()
        if self.modulebak and self.modulesGroup:
            for modules in self.modulesGroup:
                self.workflow.removeModules(modules)
            self.workflow.addModules(self.modulebak, self.name)


class MergeModule(Module):
    
    def __init__(self, name, require, next, workflow, data = None):
        super(MergeModule, self).__init__(name, require, next, workflow, data)
        self.count = 0

    def prepareInputOutput(self):

        if not self.moduleData.inputFiles:
            inps = [{
                'multi': True,
                'name': inp,
                'value': '',
                'title': '',
                'type': 'url'
            } for inp in self.inputMap]
            self.moduleData.addInputFiles(inps)        

        newInputs = []
        for inputfile in self.moduleData.inputFiles:
            opt = self.inputMap[inputfile['name']]
            if not opt:
                continue
            oid, oname= opt['id'], opt['name']
            if oid and oname:
                inputs = []
                for i in range(self.count):
                    mid = template % (oid, i)
                    config.Log.info('mid: %s' % mid)
                    omodule = self.workflow.getModule(mid)
                    config.Log.info('omodule: %s' % omodule)
                    assert(omodule.index == i)
                    ipt = copy.deepcopy(inputfile)
                    ipt['index'] = i
                    ipt['value'] = omodule.moduleData.getOutputFile(oname)
                    inputs.append(ipt)
                newInputs.append(inputs)

        for inputs in newInputs:
            self.moduleData.setMultiInputs(inputs)
        self.moduleData.addAllInputToOutput()

    # def reset(self):
    #     super(MergeModule, self).reset()

    def setMergeCount(self, count):
        self.count = count
