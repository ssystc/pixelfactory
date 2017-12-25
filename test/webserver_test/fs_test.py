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
from common import webos
from webserver import user
from model.workflow import WorkFlowDao, WorkFlow
from common import fs
from webserver import api
from model.logininfo import LoginInfoDao, LoginInfo
from taskserver.log import Log
import config
import os
from common import userserver

class fsTest(unittest.TestCase):
    
    config.Log = Log
    testRootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    testRootDir = testRootDir.replace('\\', '/')
    testFlowDir = '%s%s' % (testRootDir, '/testdata/simple_flow.json')
    testcontent = json.dumps(json.load(open(testFlowDir)), ensure_ascii=False)
    testWorkFlow = WorkFlow(testcontent, '200010035324693')
    testListDir = [{'path': u'testfile', 'metadataid': None, 'type': 'file', 'id': 200010035393403L}]
    
    def setUp(self):
        webserver.app.config['TESTING'] = True
        self.app = webserver.app.test_client()
        
    def test_a_PrepareDir(self):
        print u'************* 测试生成准备文件夹 *************'

        # 什么参数都没传入
        rep = self.app.post('/api/fs/dir/prepare')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoFlowIdInReq)

        # 没有传入dir参数(跟目录id)
        rep = self.app.post('/api/fs/dir/prepare',
                            data={
                                'flowId': 'testflowid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoDirInReq)

        # 无法根据session['uid']查询到用户id
        api.getUserId = mock.Mock(return_value=None)
        LoginInfoDao.queryUsernameByuserid = mock.Mock(return_value='ssy')
        userserver.getTokenByuserid = mock.Mock(return_value='testtoken')
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        rep = self.app.post('/api/fs/dir/prepare',
                            data={
                                'flowId': 'testflowid',
                                'dir': '200000000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)


        # 无法根据flowid查到workflow
        api.getUserId = mock.Mock(return_value='200010035324693')
        LoginInfoDao.queryUsernameByuserid = mock.Mock(return_value='ssy')
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        WorkFlowDao.queryWorkflow = mock.Mock(return_value=None)
        rep = self.app.post('/api/fs/dir/prepare',
                            data={
                                'flowId': 'testflowid',
                                'dir': '200000000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindFlowById)

        # 正确输入
        WorkFlowDao.queryWorkflow = mock.Mock(return_value=fsTest.testWorkFlow)
        fs.prepareDirOnWebos = mock.Mock(return_value=0)
        rep = self.app.post('/api/fs/dir/prepare',
                            data={
                                'flowId': 'testflowid',
                                'dir': '200000000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)


    def test_b_GetFsList(self):
        print u'************* 测试根据taskid查询file system 列表 *************'

        # 查询不到用户
        api.getUserId = mock.Mock(return_value='')
        rep = self.app.get('/api/fs/list/testtaskid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)

        # 根据taskid查不到task
        api.getUserId = mock.Mock(return_value='testuserid')
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        webos.listTaskDir = mock.Mock(return_value={'code': ErrorCode.NotFindTaskById})
        rep = self.app.get('/api/fs/list/testtaskid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindTaskById)

        # 正确输入
        webos.listTaskDir = mock.Mock(return_value={'code': ErrorCode.NoError})
        rep = self.app.get('/api/fs/list/testtaskid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)

    def test_c_ListInOutput(self):
        print u'************* 测试根据taskid查询input,output列表 *************'

        # 找不到user
        api.getUserId = mock.Mock(return_value=None)
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        rep = self.app.get('/api/fs/listioput/testtaskid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)

        # 正常输入
        webos.listInputOutputDir = mock.Mock(return_value={'code': 0})
        api.getUserId = mock.Mock(return_value='200010035324693')
        rep = self.app.get('/api/fs/listioput/testtaskid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)

    def test_d_ListByDirId(self):
        print u'************* 测试根据Dirid查询其下文件（夹）列表 *************'

        # 找不到user
        api.getUserId = mock.Mock(return_value=None)
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        rep = self.app.get('/api/fs/listbydirid/testdirid')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)

        # 正常输入
        webos.listDirByDirId = mock.Mock(return_value=[])
        api.getUserId = mock.Mock(return_value='200010035324693')
        rep = self.app.get('/api/fs/listbydirid/testdirid')
        self.assertEqual(rep.data, '[]\n')

    def test_e_ListInput(self):
        print u'************* 测试根据Dirid查询Input文件 *************'

        # 找不到user
        api.getUserId = mock.Mock(return_value=None)
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        rep = self.app.post('/api/fs/listinput')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)

        # 输入正确时
        api.getUserId = mock.Mock(return_value='200010035324693')
        webos.listDir = mock.Mock(return_value=fsTest.testListDir)
        rep = self.app.post('/api/fs/listinput',
                            data={
                                'dirid': '200000000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj[0]['id'], 200010035393403)

    def test_f_List(self):
        print u'************* 测试根据Dirid查询其下文件 *************'

        # 找不到user
        api.getUserId = mock.Mock(return_value=None)
        api.getTokenByuserid = mock.Mock(return_value='testtoken')
        rep = self.app.post('/api/fs/list')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NotFindUser)

        # 输入正确时
        api.getUserId = mock.Mock(return_value='200010035324693')
        webos.listDir = mock.Mock(return_value=fsTest.testListDir)
        rep = self.app.post('/api/fs/list',
                            data={
                                'dirid': '200000000'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj[0]['id'], 200010035393403)
        

if __name__ == '__main__':
    unittest.main()

        
        
        
        
        
        
        

