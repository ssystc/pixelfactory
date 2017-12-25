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


class workflowTest(unittest.TestCase):

    config.Log = Log
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # test文件夹路径
    testRootDir = testRootDir.replace('\\', '/')
    testRightTaskobj = json.load(open('%s%s' % (testRootDir, '/testdata/right_task.json')))
    testRightWorkFlowboj = json.load(open('%s%s' % (testRootDir, '/testdata/right_flow.json')))

    testRightWorkFlow = workflow.Workflow(testRightTaskobj, testRightWorkFlowboj, '200010035324693')
    
    testRightOCModuleData = moduledata.ModuleData(file=open('%s%s' % (testRootDir, '/testdata/right_OC.json')))
    testRightRSModuleData = moduledata.ModuleData(file=open('%s%s' % (testRootDir, '/testdata/right_RS.json')))
    testRightLLtsModuleOC = lltsmodule.LLTSModule(
        'OCtestmodule', ['__start_module__'], ['RStestmodule'],
        testRightWorkFlow, testRightOCModuleData)
    testRightBaseModuleOC = lltsmodule.Module(
        'OCtestmodule', ['__start_module__'], ['RStestmodule'],
        testRightWorkFlow, testRightOCModuleData)
    testRightBaseModuleRS = lltsmodule.Module(
        'RStestmodule', ['OCtestmodule'], ['__end_module__'],
        testRightWorkFlow, testRightRSModuleData)
    
    class testDuplicateModule():
        name = '__end_module__'
    
    
    def test_a_AddAndRemoveModule(self):
        print u'*************** 测试向WorkFlow中添加和移除Module ***************'


        # 向WrokFlow中添加重复模块时
        code = workflow.Workflow.addModule(workflowTest.testRightWorkFlow, workflowTest.testDuplicateModule)
        self.assertEqual(code, ErrorCode.DuplicateModule)

        # 正确的添加一个module情况
        code = workflow.Workflow.addModule(workflowTest.testRightWorkFlow, workflowTest.testRightBaseModuleOC)
        code2 = workflow.Workflow.addModule(workflowTest.testRightWorkFlow, workflowTest.testRightBaseModuleRS)
        self.assertEqual(code, code2, ErrorCode.NoError)

        # GetModule的根据名字得到module的信息
        self.assertTrue(workflow.Workflow.getModule(workflowTest.testRightWorkFlow, '__start_module__'))
        self.assertTrue(workflow.Workflow.getModule(workflowTest.testRightWorkFlow, 'OCtestmodule'))
        self.assertFalse(workflow.Workflow.getModule(workflowTest.testRightWorkFlow, '__None_module__'))

        # 根据modules的name移除
        workflow.Workflow.removeModules(workflowTest.testRightWorkFlow, ['OCtestmodule', 'RStestmodule'])
        obj = workflowTest.testRightWorkFlow.modules
        self.assertEqual(obj['__end_module__'].require, obj['__start_module__'].next, [])
        self.assertFalse('OCtestmodule' in obj)
        self.assertFalse('RStestmodule' in obj)

        # addModules添加多个module
        workflow.Workflow.addModules(workflowTest.testRightWorkFlow,
                            {'OCtestmodule': workflowTest.testRightBaseModuleOC,
                             'RStestmodule': workflowTest.testRightBaseModuleRS},
                            None)
        obj = workflowTest.testRightWorkFlow.modules
        self.assertTrue('OCtestmodule' in obj)
        self.assertTrue('RStestmodule' in obj)


    def test_b_GetSomeInfo(self):
        print u'*************** 测试获取start和end module；测试判断以及设置module状态为Ready ***************'

        # get Start or End module
        self.assertEqual(workflow.Workflow.getStartModule(workflowTest.testRightWorkFlow).name, '__start_module__')
        self.assertEqual(workflow.Workflow.getEndModule(workflowTest.testRightWorkFlow).name, '__end_module__')

        # get modulstate,且module在modules中
        code = workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, 'OCtestmodule')
        self.assertEqual(code, 0)
        # get modulstate,且module不在modules中
        code = workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, 'SomeErrorName')
        self.assertEqual(code, -1)

        # canModuleReady,是否可以将模块设为Ready
        self.assertEqual(workflow.Workflow.canModuleReady(workflowTest.testRightWorkFlow, 'unknownmodule'), False)
        self.assertEqual(workflow.Workflow.canModuleReady(workflowTest.testRightWorkFlow, 'testmodule'), False)
        workflowTest.testRightWorkFlow.modules['RStestmodule'].state = 3
        self.assertEqual(workflow.Workflow.canModuleReady(workflowTest.testRightWorkFlow, '__end_module__'), True)

        # _setModuleReady
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), None)
        workflow.Workflow._setModuleReady(workflowTest.testRightWorkFlow, ['__end_module__'])
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 1)

    def test_c_RunReadyModule(self):
        print u'*************** 测试获取_runReadyModule ***************'
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 1)
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, 'RStestmodule'), 3)
        workflow.Workflow._runReadyModule(workflowTest.testRightWorkFlow)
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 2)
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, 'RStestmodule'), 3)

    def test_d_CheckFinished(self):
        print u'*************** 测试获取_checkFinished ***************'
        basemodule.Module.getlltsId = mock.Mock(return_value=1234567)
        StateClanDao.addStateClan = mock.Mock(return_value=None)
        # 没有错误时
        self.assertEqual(workflow.Workflow._checkFinished(workflowTest.testRightWorkFlow), (True, False))
        # 没有模块处于Runing状态
        self.assertEqual(workflow.Workflow._checkFinished(workflowTest.testRightWorkFlow), (False, False))
        # 返回值出现错误时
        workflowTest.testRightWorkFlow.modules['__end_module__'].state = 2
        basemodule.Module.hasError = mock.Mock(return_value='testErrorCode')
        self.assertEqual(workflow.Workflow._checkFinished(workflowTest.testRightWorkFlow), (True, True))

    def test_e_RunNext(self):
        print u'*************** 测试_runNext ***************'
        # _runNext
        workflow.Workflow.saveWorkflowState = mock.Mock(return_value=None)
        workflowTest.testRightWorkFlow.modules['__end_module__'].state = 1
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 1)
        workflow.Workflow._runNext(workflowTest.testRightWorkFlow)
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 4)

        # 没有hasError时
        workflowTest.testRightWorkFlow.modules['__end_module__'].state = 1
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 1)
        basemodule.Module.hasError = mock.Mock(return_value=None)
        workflow.Workflow._runNext(workflowTest.testRightWorkFlow)
        self.assertEqual(workflow.Workflow.getModuleState(workflowTest.testRightWorkFlow, '__end_module__'), 3)

    def test_f_hasError(self):
        print u'*************** 测试hasError以及formatError ***************'
        # 完全没有错误时
        self.assertEqual(workflow.Workflow.hasError(workflowTest.testRightWorkFlow), False)
        self.assertEqual(workflow.Workflow.formatError(workflowTest.testRightWorkFlow), '')

        # 有errorCode时
        workflowTest.testRightWorkFlow.errorCode = 'testErrorCode'
        self.assertEqual(workflow.Workflow.hasError(workflowTest.testRightWorkFlow), True)
        self.assertTrue('testErrorCode' in workflow.Workflow.formatError(workflowTest.testRightWorkFlow))

        # 没有errorCode但是存在module的State为4，即某个module存在错误时
        workflowTest.testRightWorkFlow.errorCode = None
        workflowTest.testRightWorkFlow.modules['__end_module__'].state = 4
        self.assertEqual(workflow.Workflow.hasError(workflowTest.testRightWorkFlow), True)
        self.assertTrue('__end_module__' in workflow.Workflow.formatError(workflowTest.testRightWorkFlow))

    def test_g_OperateRun(self):
        print u'*************** 测试start,stop,pause,continue ***************'
        # start
        workflow.Workflow.start = mock.Mock(return_value=None)
        self.assertEqual(workflow.Workflow.startRun(workflowTest.testRightWorkFlow), 0)
        self.assertEqual(workflowTest.testRightWorkFlow._pause, workflowTest.testRightWorkFlow._stop, False)
        self.assertEqual(workflowTest.testRightWorkFlow._taskStateId, None)
        self.assertEqual(workflowTest.testRightWorkFlow._dirInit, False)
        # pause
        self.assertEqual(workflow.Workflow.pauseRun(workflowTest.testRightWorkFlow), 0)
        self.assertEqual(workflowTest.testRightWorkFlow._pause, True)
        # continue
        self.assertEqual(workflow.Workflow.continueRun(workflowTest.testRightWorkFlow), 0)
        self.assertEqual(workflowTest.testRightWorkFlow._pause, False)
        # stop
        self.assertEqual(workflow.Workflow.stopRun(workflowTest.testRightWorkFlow), 0)
        self.assertEqual(workflowTest.testRightWorkFlow._stop, True)


    def test_h_GetState(self):
        print u'*************** 测试getState ***************'
        workflow.Workflow.getTaskId = mock.Mock(return_value='testTaskId')
        basemodule.Module.exitCode = mock.Mock(return_value=0)
        lltsmodule.LLTSModule.exitCode = mock.Mock(return_value=0)
        self.assertEqual(workflow.Workflow.getState(workflowTest.testRightWorkFlow)['RStestmodule']['code'], 0)

if __name__ == '__main__':
    unittest.main()
