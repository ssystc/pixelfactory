# coding: utf-8

import unittest
import uuid
import requests

class UiDataTest(unittest.TestCase):

    host = 'http://localhost:8081/api/flow/ui/data'
    flowId = uuid.uuid4().hex

    def testSetData(self):
        print u'测试添加数据'
        content = 'testcontent'
        rep = requests.post(UiDataTest.host, data = [
            ('flowId', UiDataTest.flowId),
            ('content', content)
        ])
        self.assertEqual(rep.status_code, 200)
        print rep.content

        print u'测试修改数据'
        content = 'testcontent2'
        rep = requests.post(UiDataTest.host, data = [
            ('flowId', UiDataTest.flowId),
            ('content', content)
        ])
        self.assertEqual(rep.status_code, 200)
        print rep.content

    def testGetData(self):
        print u'测试获取数据'
        rep = requests.get('%s/%s' % (UiDataTest.host, UiDataTest.flowId))
        self.assertEqual(rep.status_code, 200)
        print rep.content

