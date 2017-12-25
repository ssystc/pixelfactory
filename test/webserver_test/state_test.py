#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import webserver
import unittest
import mock
import json
from common.const import ErrorCode
from model.stateclan import StateClan, StateClanDao
from model.taskstate import TaskStateDao, TaskState
from model.task import Task, TaskDao


class stateTest(unittest.TestCase):

    testClan = '{"errorCode": 0, "fileuploading": true, "OC37b7a0ab-9638-4081-9119-2ced1b815261-1": {"code": 3, "uploading": true, "detail": "TASK_1505808395.05_JQqeO", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}, "OC37b7a0ab-9638-4081-9119-2ced1b815261-0": {"code": 3, "uploading": true, "detail": "TASK_1505808395.34_jHcQf", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}, "errorMessage": "", "RSUniformColorb465b328-e477-4d04-a914-32ddac803650-0": {"code": 3, "uploading": true, "detail": "TASK_1505808639.91_jTaMZ", "returnCode": 0, "returnMsg": "Process success.", "fsid": null, "exitCode": 0}, "paused": false, "0dc9d7fb-150d-4922-bd90-ae068f178a1f": {"code": 3, "uploading": false, "detail": null, "returnCode": 0, "returnMsg": "", "fsid": null, "exitCode": 0}, "state": 2, "RSUniformColorb465b328-e477-4d04-a914-32ddac803650-1": {"code": 3, "uploading": true, "detail": "TASK_1505808624.6_dbwev", "returnCode": 0, "returnMsg": "Process success.", "fsid": null, "exitCode": 0}, "GSImageSharpenDistribut6ca0c501-9edd-40ef-875b-1c0863c3435d-1": {"code": 3, "uploading": true, "detail": "TASK_1505808455.01_ritKy", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}, "GSImageSharpenDistribut6ca0c501-9edd-40ef-875b-1c0863c3435d-0": {"code": 3, "uploading": true, "detail": "TASK_1505808450.3_jLYbO", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}, "taskId": "191c9384828a49c3abcafa9b2154226b", "__start_module__": {"code": 3, "uploading": false, "detail": null, "returnCode": 0, "returnMsg": "", "fsid": null, "exitCode": 0}, "__end_module__": {"code": 3, "uploading": false, "detail": null, "returnCode": 0, "returnMsg": "", "fsid": null, "exitCode": 0}, "OCec44884e-ac24-4130-80b1-fa3827b8682c-1": {"code": 3, "uploading": true, "detail": "TASK_1505808395.64_OZayy", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}, "OCec44884e-ac24-4130-80b1-fa3827b8682c-0": {"code": 3, "uploading": true, "detail": "TASK_1505808395.92_heThL", "returnCode": 0, "returnMsg": "SUCCESS", "fsid": null, "exitCode": 0}}'
    testTaskState = TaskState('testtaskid', 0, 0.0, 1.0, 2.0, testClan, '-2', '200010035324693')
    testStateClan = StateClan('uid', 'testtaskId', 'testclan', '200010035324693', 'ssy', 0.0, 1.0)
    testStateClanList = [testStateClan]
    
    def setUp(self):
        webserver.app.config['TESTING'] = True
        self.app = webserver.app.test_client()
    
    def test_a_GetTaskState(self):
        print u'*********** 测试根据taskId查询taskstate信息 ***********'
        
        # 传入无效的taskid
        TaskStateDao.lastTaskState = mock.Mock(return_value=None)
        rep = self.app.get('/api/task/state/testid')
        self.assertEqual(rep.data, '{}\n')
        
        # 传入有效地taskid
        TaskStateDao.lastTaskState = mock.Mock(return_value=stateTest.testTaskState)
        rep = self.app.get('/api/task/state/testid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['runTime'], 1.0)
        
        
    def test_b_GetStateClan(self):
        print u'*********** 测试根据taskId查询stateclan信息 ***********'
        
        # 没有传入taskid
        rep = self.app.post('/api/stateclan/query')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoTaskIdInReq)
        
        # 传入的taskid在stateclan表中无法查到相应数据
        StateClanDao.queryByTaskId = mock.Mock(return_value=None)
        rep = self.app.post('/api/stateclan/query',
                            data={
                                'taskid': 'testtaskid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindStateClanByTask)

        # 传入taskid且能在stateclan表中查询到相应数据
        StateClanDao.queryByTaskId = mock.Mock(return_value=stateTest.testStateClanList)
        rep = self.app.post('/api/stateclan/query',
                            data={
                                'taskid': 'testtaskid'
                            })
        obj = json.loads(rep.data)
        self.assertTrue(obj['ssy'])
        
    def test_b_QueryTaskStatus(self):
        print u'*********** 测试根据flowId查询task运行状态信息 ***********'
        
        # 没有传入flowid
        rep = self.app.post('/api/taskstatus/query')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoFlowIdInReq)
        
        # 传入了flowid，但该Id在查不到对应的task
        TaskDao.queryTaskIdByFlowId = mock.Mock(return_value=[])
        rep = self.app.post('/api/taskstatus/query',
                            data={
                                'flowid': 'testflowid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindTaskByFlowId)
        
        # 传入了flowid，也能查询到对应的task，但是根据查到的taskid无法查到taskstate
        TaskDao.queryTaskIdByFlowId = mock.Mock(return_value=[1])
        TaskStateDao.lastTaskState = mock.Mock(return_value=None)
        rep = self.app.post('/api/taskstatus/query',
                            data={
                                'flowid': 'testflowid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['1'], 'NotRuning')

        # 传入了flowid，也能查询到对应的task，根据查到的taskid可以查到taskstate
        TaskStateDao.lastTaskState = mock.Mock(return_value=stateTest.testTaskState)
        rep = self.app.post('/api/taskstatus/query',
                            data={
                                'flowid': 'testflowid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['testtaskid'], 'NotRuning')
        
        
        
if __name__ == '__main__':
    unittest.main()
        
        

