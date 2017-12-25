#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import mock
import unittest
import json
from taskserver import basemodule, lltsmodule, workflow, workflowdata, moduledata
import config
from taskserver.log import Log
from common import llts
import os

class moduleTest(unittest.TestCase):
    
    config.Log = Log
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testRootDir = testRootDir.replace('\\', '/')

    testRightTaskobj = json.load(open('%s%s' % (testRootDir, '/testdata/right_task.json')))
    testRightWorkFlowboj = json.load(open('%s%s' % (testRootDir, '/testdata/right_flow.json')))
    testRightWorkFlow = workflow.Workflow(testRightTaskobj, testRightWorkFlowboj, '200010035324693')
    testRightModuleData = moduledata.ModuleData(file=open('%s%s' % (testRootDir, '/testdata/right_OC.json')))
    testRightRsModuleData = moduledata.ModuleData(file=open('%s%s' % (testRootDir, '/testdata/right_RS.json')))
    testRightLLtsModule = lltsmodule.LLTSModule('OCaac62df3-3cb7-4488-ada7-847d922eb46c', ['__start_module__'], ['GS'], testRightWorkFlow, testRightModuleData)
    testRightBaseModule = lltsmodule.Module('OCaac62df3-3cb7-4488-ada7-847d922eb46c', ['__start_module__'], ['GS'], testRightWorkFlow, testRightModuleData)
    testRightBaseModuleMultiIsTrue = lltsmodule.Module('RS255qdafasdg', ['__start_module__'], ['GS'], testRightWorkFlow, testRightRsModuleData)
    def test_a_lltsmd_isFinished(self):
        print '***************** 测试lltsModule中的isFinished方法 *****************'
        
        # lltsId = None,-1,-2的情况
        lltsIdList = [None, -1, -2]
        myresult = [True, True, False]
        i = 0
        for lltsid in lltsIdList:
            moduleTest.testRightLLtsModule.lltsId = lltsid
            self.assertEqual(lltsmodule.LLTSModule.isFinished(moduleTest.testRightLLtsModule), myresult[i])
            i = i+1
            
        # common.llts.start()，得到一个真实的lltsId之后
        moduleTest.testRightLLtsModule.lltsId = 'testLLtsId'
        testState1 = {'__STATUS__': 'FINISHED', '__EXIT_CODE__': 0}
        testState2 = {'__STATUS__': 'ENDED', '__EXIT_CODE__': 12345}
        testState3 = {'__STATUS__': 'ELSESTATUS', '__EXIT_CODE__': 54321}
        llts.getState = mock.Mock(side_effect=[testState1, testState2, testState3])
        for i in range(3):
            #三次不同的lltsId的预期结果也是[True, True, False]
            self.assertEqual(lltsmodule.LLTSModule.isFinished(moduleTest.testRightLLtsModule), myresult[i])
            
    def test_b_getOutPut(self):
        print '***************** 测试baseModule中的_getOutput(s) *****************'
        
        #传入正确的或错误的output name时,测试_getOutput
        rightvalue = 'E:\\VMcentosShare\\GF\\ZY3_2\\result\\ZY3_TLC_E116.0_N39.8_20120417_L1A0000921343-NAD_ziji\\ZY3_TLC_E116.0_N39.8_20120417_L1A0000921343-NAD_OC.tiff'
        self.assertEqual(basemodule.Module._getOutput(moduleTest.testRightBaseModule, 'OutputImgFileName'), rightvalue)
        self.assertEqual(basemodule.Module._getOutput(moduleTest.testRightBaseModule, 'ErrorFileName'), None)
        
        #测试_getOutputs
        self.assertTrue(basemodule.Module._getOutputs(moduleTest.testRightBaseModule, 'OutputImgFileName')[0])
        self.assertEqual(basemodule.Module._getOutputs(moduleTest.testRightBaseModule, 'ErrorName'), [])
        
    def test_c_PrepareInput(self):
        print '***************** 测试baseModule中的_prepareInput *****************'
        # multi = False
        basemodule.Module._getInputValueFromInputMap = mock.Mock(return_value='tsetValue')
        basemodule.Module._prepareInput(moduleTest.testRightBaseModule)
        list = moduleTest.testRightLLtsModule.moduleData.inputFiles
        self.assertEqual(list[0]['value'], list[1]['value'], 'testValue')

        # multi = True
        basemodule.Module._getInputsFromInputMap = mock.Mock(return_value=[{'name': 'InputImgFileName'}])
        moduledata.ModuleData.setMultiInputs = mock.Mock(return_value=True)
        basemodule.Module._prepareInput(moduleTest.testRightBaseModuleMultiIsTrue)


if __name__ == '__main__':
    unittest.main()
