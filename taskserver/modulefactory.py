# coding: utf-8

from restmodule import RestModule
from lltsmodule import LLTSModule
from parallelmodule import MergeModule, ParallelStartModule
import config

moduleConfig = {
    'rest': RestModule,
    'llts': LLTSModule,
    'parallel': ParallelStartModule,
    'merge': MergeModule
}

def createModule(moduleClass, name, require, next, workflow, data = None):
    config.Log.info('create module %s', moduleClass)
    if moduleClass in moduleConfig:
        module = moduleConfig[moduleClass](name, require, next, workflow, data)
        config.Log.info(module)
        return module
    config.Log.error("can't create module %s", moduleClass)
    return None
