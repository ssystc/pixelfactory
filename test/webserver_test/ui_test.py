#coding=utf-8
import sys
sys.path.append("./")

import unittest
import webserver
import mock
from model.uidata import UiData, UiDataDao
import json
from common.const import ErrorCode


class uiTest(unittest.TestCase):
    
    def setUp(self):
        webserver.app.config['TESTING'] = True
        self.app = webserver.app.test_client()
        
    def test_a_GetUiData(self):
        print u'********** 根据ui的id获取ui列表 **********'
        UiDataDao.getData = mock.Mock(return_value='testcontent')
        rep = self.app.get('/api/flow/ui/data/testuiid')
        self.assertEqual(rep.data, 'testcontent')
        
    def test_b_SetUiData(self):
        print u'********** 保存（更新）uiData **********'
        
        # 没有传入flowId
        rep = self.app.post('/api/flow/ui/data')
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoFlowIdInReq)
        
        # 没有传入content
        rep = self.app.post('/api/flow/ui/data',
                            data={
                                'flowId': 'testflowid'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoContentInReq)
        
        # 正确的传入
        UiDataDao.setData = mock.Mock(return_value=0)
        rep = self.app.post('/api/flow/ui/data',
                            data={
                                'flowId': 'testflowid',
                                'content': 'testcontent'
                            })
        obj = json.loads(rep.data)
        self.assertEqual(obj['code'], ErrorCode.NoError)
        
if __name__ == '__main__':
    unittest.main()
