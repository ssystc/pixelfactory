#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")


import mock
import os
import webserver
import unittest
import tempfile
import flask
from model import workflow
import json
from model.workflow import WorkFlow, WorkFlowDao
from model.module import Module, ModuleDao
from common import llts
from model.task import TaskDao, Task
from model.taskstate import TaskState, TaskStateDao

class workflowTest(unittest.TestCase):

    testmodulelist =[
    {
        "createDate": "",
        "desc": "",
        "icon": "",
        "id": "BundleAdj_RS-0.0.1",
        "manual": "",
        "name": "遥感卫星区域网平差",
        "owner": "",
        "redirect": "",
        "runMethod": "",
        "type": "remotesatellite"
    },
    {
        "createDate": "",
        "desc": "",
        "icon": "",
        "id": "BundleAdj_Survey-0.0.1",
        "manual": False,
        "name": "测绘卫星区域网平差",
        "owner": "",
        "redirect": "",
        "runMethod": "",
        "type": ""
    }]
    testparallel ={
        "ModuleClass": "parallel",
        "createDate": "",
        "desc": "",
        "icon": "",
        "id": "parallel",
        "manual": False,
        "name": "并行",
        "owner": "",
        "redirect": "",
        "runMethod": "",
        "type": "system"
    }
    
    testmoduleinfo ={
        "ModuleClass": "merge",
        "Userproperty": {
            "InputParameter": {
                "Configuration": [],
                "InputFilePath": []
            },
            "OutputParameter": {
                "OutPutFilePath": []
            }
        },
        "createDate": "",
        "desc": "",
        "icon": "",
        "id": "merger",
        "manual": False,
        "name": "合并",
        "op": "",
        "owner": "",
        "redirect": "",
        "type": "system",
        "version": "0.0.1"
    }
    
    testmoduleid = 'merger'
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testRootDir = testRootDir.replace('\\', '/')
    testFlowDir = '%s%s' % (testRootDir, '/testdata/simple_flow.json')
    testcontent = json.dumps(json.load(open(testFlowDir)), ensure_ascii=False)
    testWorkFlowList = [WorkFlow(testcontent, '200010035324693')]
    testWorkFlow = WorkFlow(testcontent, '200010035324693')



    def setUp(self):
        webserver.app.config['TESTING'] = True
        webserver.app.config['CSRF_ENABLED'] = False
        self.app = webserver.app.test_client()


    def tearDown(self):
        return ''

    def test_a_GetModuleList(self):
        print u'*****************测试获取所有module*****************'
        llts.getModuleList = mock.Mock(return_value=workflowTest.testmodulelist)
        ModuleDao.modulesList = mock.Mock(return_value=workflowTest.testparallel)
        rep = self.app.get('/api/module')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data, encoding='utf-8')
        self.assertTrue(obj[0]['id'])

    def test_b_GetModuleByToolId(self):
        print u'*****************测试根据toolId获取对应的module信息*****************'
        llts.getToolDetail = mock.Mock(return_value=workflowTest.testmoduleinfo)
        rep = self.app.get('api/module/testid')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertTrue(obj['id'])

    def test_c_AddWorkFlow(self):
        print u'*****************测试添加WorlFlow*****************'

        #没有传入content时
        rep = self.app.post('/api/flow')
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], -1)

        #传入content且传入flowid时
        WorkFlowDao.updateWorkflow = mock.Mock(return_value=0)
        flow = json.load(open(workflowTest.testFlowDir))
        content = json.dumps(flow, ensure_ascii=False)
        rep = self.app.post('/api/flow', data={'content': content,'id':'987654321'})
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], 0)
        self.assertEqual(obj['id'], '987654321')

        #传入的workflowID不存在于数据库中时
        WorkFlowDao.updateWorkflow = mock.Mock(return_value=-4)
        rep = self.app.post('/api/flow', data={'content': content, 'id': '987654321'})
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], -4)


        #传入content但不传入flowid时
        WorkFlowDao.saveWorkflow = mock.Mock(return_value=0)
        flow = json.load(open(workflowTest.testFlowDir))
        content = json.dumps(flow, ensure_ascii=False)
        rep = self.app.post('/api/flow', data={'content': content})
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], 0)

    def test_d_GetFlowList(self):
        print u'*****************测试获取workflow列表*****************'
        WorkFlowDao.workflowList = mock.Mock(return_value=workflowTest.testWorkFlowList)
        rep = self.app.get('/api/flow')
        self.assertEqual(rep.status_code, 200)

    def test_e_GetFlowListByKey(self):
        print u'*****************测试根据key获取workflow列表*****************'
        WorkFlowDao.queryByKey = mock.Mock(return_value=workflowTest.testWorkFlowList)
        rep = self.app.get('/api/flow/testkey')
        self.assertEqual(rep.status_code, 200)
        
        #没有该key时
        WorkFlowDao.queryByKey = mock.Mock(return_value=[])
        rep = self.app.get('/api/flow/testkey')
        self.assertEqual(rep.status_code, 200)

    def test_f_GetFlowById(self):
        print u'*****************测试根据flowId获取workflow信息*****************'

        #根据id查的到
        WorkFlowDao.queryWorkflow = mock.Mock(return_value=workflowTest.testWorkFlow)
        rep = self.app.get('/api/flow/testid')
        self.assertEqual(rep.status_code, 200)

        #根据id查不到
        WorkFlowDao.queryWorkflow = mock.Mock(return_value={})
        rep = self.app.get('/api/flow/testid')
        self.assertEqual(rep.status_code, 200)
        self.assertEqual(json.loads(rep.data), {})

    def test_g_DelFlowById(self):
        print u'*****************测试根据flowId删除workFlow*****************'
        #如果没有传入flowId
        rep = self.app.delete('/api/flow', data={})
        self.assertEqual(json.loads(rep.data)['code'], -2)
        
        #正确情况
        WorkFlowDao.deleteUiDataByFlowId = mock.Mock(return_value=0)
        TaskDao.queryTaskIdByFlowId = mock.Mock(return_value=[1,2])
        TaskStateDao.deleteTaskState = mock.Mock(return_value=0)
        TaskDao.deleteByFlowId = mock.Mock(return_value=0)
        WorkFlowDao.deleteWorkflow = mock.Mock(return_value=0)
        rep = self.app.delete('/api/flow', data={'id': 'testid'})
        self.assertEqual(json.loads(rep.data)['code'], 0)


if __name__ == '__main__':
    unittest.main()


