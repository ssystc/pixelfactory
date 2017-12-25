#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import unittest
import json
import webserver
import mock
from common.const import ErrorCode
from model.task import TaskDao, Task
from webserver import user
from model.workflow import WorkFlowDao, WorkFlow
from model.taskstate import TaskStateDao, TaskState
import os


class taskTest(unittest.TestCase):
    
    testTaskJson = {
    "id": "",
    "name": "测试任务",
    "desc": "测试流程的任务",
    "owner": "ssy",
    "createDate": "2017.08.08",
    "flowId": "5070cb4a6e03464d8b4583ab069cca67",
    "dir": "/home/llts/lzz/data",
    "args": [
        { "name": "tiffFile", "title": "输入影像文件", "type": "string", "value": "", "auto":["_transtiff.tiff"] }
    ]
}
    testTask = Task(json.dumps(testTaskJson, ensure_ascii=False), '200010035324693')
    testTaskList = [testTask]
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testRootDir = testRootDir.replace('\\', '/')
    testFlowDir = '%s%s' % (testRootDir, '/testdata/simple_flow.json')
    testcontent = json.dumps(json.load(open(testFlowDir)), ensure_ascii=False)
    testWorkFlow = WorkFlow(testcontent, '200010035324693')
    
    def setUp(self):
        webserver.app.config['TESTING'] = True
        webserver.app.config['CSRF_ENABLED'] = False
        self.app = webserver.app.test_client()
    
    def test_a_Addtask(self):
        print u'****** 测试添加task ******'

        # 没有传入content
        user.getUserId = mock.Mock(return_value='200010035324693')
        rep = self.app.post('/api/task')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoContentInReq)


        # 传入content且没传入taskid时
        TaskDao.saveTask = mock.Mock(return_value=0)
        content = json.dumps(taskTest.testTaskJson)
        rep = self.app.post('/api/task',
                            data={
                                'content': content
                            })
        obj = json.loads(rep.data)
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(obj['code'], ErrorCode.NoError)

        # 传入content且传入一个已存在于数据库中的taskid
        TaskDao.updateTask = mock.Mock(return_value=0)
        rep = self.app.post('/api/task',
                            data={
                                'content': content,
                                'id': 'testid'
                            })
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], 0)
        self.assertEqual(obj['id'], 'testid')

        # 传入content且传入一个不存在于数据库中的taskid
        TaskDao.updateTask = mock.Mock(return_value=ErrorCode.NotFindTaskById)
        rep = self.app.post('/api/task',
                            data={
                                'content': content,
                                'id': 'testid'
                            })
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindTaskById)
        self.assertEqual(obj['id'], 'testid')

    def test_b_GetTaskList(self):
        print u'****** 测试根据flowId获取task列表 ******'

        # 没有传入flowId
        rep = self.app.get('/api/task')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoFlowIdInReq)

        # 传入flowId
        TaskDao.taskList = mock.Mock(return_value=taskTest.testTaskList)
        rep = self.app.get('/api/task?flowId=testflowid')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertTrue('id' in obj[0])


    def test_c_GetTaskInfo(self):
        print u'****** 测试根据taskId获取task信息 ******'

        TaskDao.queryTask = mock.Mock(return_value=taskTest.testTask)
        rep = self.app.get('/api/task/testid')
        self.assertTrue(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertTrue('id' in obj)

    def test_d_DelTask(self):
        print u'****** 测试根据taskId删除task ******'

        # 没有传入taskid
        rep = self.app.delete('/api/task', data={})
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)

        # 传入了taskid
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=0)
        TaskStateDao.deleteTaskState = mock.Mock(return_value=0)
        TaskDao.deleteTask = mock.Mock(return_value=0)
        rep = self.app.delete('/api/task',
                              data={
                                  'id': 'testid'
                              })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], 0)

    def test_e_StartTask(self):
        print u'****** 开始任务 ******'

        # 没有传入taskId
        rep = self.app.post('/api/task/start')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)

        # 无法根据taskId在数据库中查到对应的task
        TaskDao.queryTask = mock.Mock(return_value=None)
        rep = self.app.post('/api/task/start',
                            data={
                                'id': 'testid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindTaskById)

        # 无法根据查到的task中的flowid查到对应的flow
        webserver.api.getUserId = mock.Mock(return_value='testUserId')
        TaskDao.queryTask = mock.Mock(return_value=taskTest.testTask)
        WorkFlowDao.queryWorkflow = mock.Mock(return_value=None)
        rep = self.app.post('/api/task/start',
                            data={
                                'id': '200000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindFlowById)

        # 传入正确的值
        WorkFlowDao.queryWorkflow = mock.Mock(return_value=taskTest.testWorkFlow)
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': 0}))
        rep = self.app.post('/api/task/start',
                            data={
                                'id': '200000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], 0)


    def test_f_PauseTask(self):
        print u'****** 暂停任务 ******'

        # 没有传入taskId
        rep = self.app.post('/api/task/pause')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)

        # 传入正确的值，但是_requestTaskServerRetCode时出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.ExceptionError}))
        rep = self.app.post('/api/task/pause',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.ExceptionError)

        # 传入正确的值，且没有出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.NoError}))
        rep = self.app.post('/api/task/pause',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)

    def test_g_ContinueTask(self):
        print u'****** 继续任务 ******'

        # 没有传入taskId
        rep = self.app.post('/api/task/contine')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)

        # 传入正确的值，但是_requestTaskServerRetCode时出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.ExceptionError}))
        rep = self.app.post('/api/task/contine',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.ExceptionError)

        # 传入正确的值，且没有出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.NoError}))
        rep = self.app.post('/api/task/contine',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)

    def test_g_StopTask(self):
        print u'****** 停止任务 ******'
    
        # 没有传入taskId
        rep = self.app.post('/api/task/stop')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)
    
        # 传入正确的值，但是_requestTaskServerRetCode时出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.ExceptionError}))
        rep = self.app.post('/api/task/stop',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.ExceptionError)
    
        # 传入正确的值，且没有出现异常
        webserver.api._requestTaskServerRetCode = mock.Mock(return_value=json.dumps({'code': ErrorCode.NoError}))
        rep = self.app.post('/api/task/stop',
                            data={
                                'id': 'testtaskId'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)

        
        
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
        
        
        


        


        
        
        
        
  
    

