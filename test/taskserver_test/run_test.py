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
from common.const import ErrorCode
from model.stateclan import StateClanDao
from model.logininfo import LoginInfoDao
import time
from common.error import MsgException
from common.const import ErrorCode


class workflowTest(unittest.TestCase):

    config.Log = Log
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # test文件夹路径
    testRootDir = testRootDir.replace('\\', '/')
    testRightTaskobj = json.load(open('%s%s' % (testRootDir, '/testdata/right_task.json')))


    def test_i_InitModules(self):
        print u'*************** 测试initModules ***************'

        flowJsonDir = '%s%s' % (workflowTest.testRootDir, '/testdata/flowJson')

        for flow in os.listdir(flowJsonDir):
            flowJson = '%s%s%s' % (flowJsonDir, '/', flow)
            testTaskObj = workflowTest.testRightTaskobj
            testWorkflowObj = json.load(open(flowJson))
            testWorkFlow = workflow.Workflow(testTaskObj, testWorkflowObj, '200010035324693')


            # flow是错误的时候
            if flow == 'flow_nomoduleclass.json':
                self.assertRaises(MsgException, workflow.Workflow.initModules, testWorkFlow)

            # 没有错误时
            else:
                self.assertFalse('dc6a6b0b-8f1d-4f91-83ef-dea7b6f1e698' in testWorkFlow.modules)
                workflow.Workflow.initModules(testWorkFlow)
                self.assertTrue('dc6a6b0b-8f1d-4f91-83ef-dea7b6f1e698' in testWorkFlow.modules)

    def test_j_startRun(self):
        print u'*************** 测试Run ***************'
        # config.Log.info = mock.Mock(return_value=None)
        workflow.Workflow.prepareFsDir = mock.Mock(return_value=None)
        workflow.Workflow.saveWorkflowState = mock.Mock(return_value=None)
        lltsmodule.createDir = mock.Mock(return_value=None)
        moduledata.ModuleData.saveToFile = mock.Mock(return_value=None)
        llts.start = mock.Mock(return_value='testlltsId')
        lltsmodule.LLTSModule.isFinished = mock.Mock(return_value=True)
        lltsmodule.LLTSModule.onFinished = mock.Mock(return_value=None)
        StateClanDao.addStateClan = mock.Mock(return_value=None)


        flowJsonDir = '%s%s' % (workflowTest.testRootDir, '/testdata/flowJson')
        flowJsonDir = flowJsonDir.replace('\\', '/')

        for flow in os.listdir(flowJsonDir):
            print flow
            flowJson = '%s%s%s' % (flowJsonDir, '/', flow)
            testTaskObj = workflowTest.testRightTaskobj
            testWorkflowObj = json.load(open(flowJson))
            testWorkFlow = workflow.Workflow(testTaskObj, testWorkflowObj, '200010035324693')

            if flow == 'flow_nomoduleclass.json':
                testWorkFlow._dirInit = True
                workflow.Workflow.startRun(testWorkFlow)
                while not testWorkFlow.finishedTime:
                    time.sleep(0.1)
                self.assertEqual(testWorkFlow.errorCode, ErrorCode.ConnectModuleError)

            elif flow == 'right_flow.json':
                testWorkFlow._dirInit = True
                workflow.Workflow.startRun(testWorkFlow)
                while not testWorkFlow.finishedTime:
                    time.sleep(0.1)
                self.assertEqual(testWorkFlow.errorCode, ErrorCode.NoError)
    
        
if __name__ == '__main__':
    unittest.main()
