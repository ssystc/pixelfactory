#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")


import mock
import unittest
from taskserver.taskmgr import TaskMgr
import json
from model.logininfo import LoginInfoDao, LoginInfo
from model.stateclan import StateClanDao, StateClan
from taskserver import workflow
import config
from taskserver.log import Log
config.Log = Log
from common.const import ErrorCode



class taskmgrTest(unittest.TestCase):
    
    
    mytestMsgDir = './test/testdata/msg.json'
    mytestMessage = json.load(open(mytestMsgDir))
    mytestWorkFlow = workflow.Workflow
    
    def test_a_StartTask(self):
        print u'*************** 测试taskserver.taskmgr.TaskMgr.StartTask ***************'
        
        # 任务已经在运行了
        StateClanDao.deleteByTaskId = mock.Mock(return_value=None)
        TaskMgr.tasks = {'67336c8a9e534a1f90f47260dcb699d5': taskmgrTest.mytestWorkFlow}
        workflow.Workflow.isOver = mock.Mock(return_value=False)
        obj = TaskMgr.startTask(taskmgrTest.mytestMessage)
        self.assertEqual(obj['__CODE__'], ErrorCode.TaskAlreadyInRuning)
        
        #任务没有在运行,但是查询不到userId
        TaskMgr.tasks = {'11111111111111111': taskmgrTest.mytestWorkFlow}
        LoginInfoDao.getUserId = mock.Mock(return_value=None)
        obj = TaskMgr.startTask(taskmgrTest.mytestMessage)
        self.assertEqual(obj['__CODE__'], ErrorCode.TaskStartNoUser)

        # 任务没有在运行,能查询到userId,正确情况
        TaskMgr.tasks = {'11111111111111111': taskmgrTest.mytestWorkFlow}
        LoginInfoDao.getUserId = mock.Mock(return_value='testuserid')
        workflow.Workflow.startRun = mock.Mock(return_value=0)
        obj = TaskMgr.startTask(taskmgrTest.mytestMessage)
        self.assertEqual(obj['__CODE__'], ErrorCode.NoError)
        
if __name__ == '__main__':
    unittest.main()
        
        

        

    
    

