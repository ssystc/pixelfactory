# encoding: utf-8

import unittest
import requests
import json

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class TestApi(unittest.TestCase):

    host = 'http://localhost:8081'
    flowId = 0

    def testAddWorkFlow(self):
        print u'测试添加流程'
        flow = json.load(open('../flow.json'))
        content = json.dumps(flow, indent=4, ensure_ascii=False)
        rep = requests.post("%s%s" % (TestApi.host, '/api/flow'), data=[
            ('content', content)
        ])
        self.assertEqual(rep.status_code, 200)

        obj = json.loads(rep.content)
        self.assertTrue('id' in obj and 'code' in obj)
        self.assertEqual(obj['code'], 0)

        flowId = obj['id']
        TestApi.flowId = flowId

        print u'测试修改流程'
        rep = requests.post("%s%s" % (TestApi.host, '/api/flow'), data = [
            ('content', content),
            ('id', flowId)
        ])
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.content)
        self.assertTrue('id' in obj and 'code' in obj)
        self.assertEqual(obj['code'], 0)

    def testGetWorkFlowList(self):
        print u'测试获取流程列表'
        rep = requests.get("%s%s" % (TestApi.host, '/api/flow'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def testGetWorkFlow(self):
        print u"测试获取流程%s" % '3e6effcf99e642569b0c12b27c457ecf'
        rep = requests.get("%s%s/%s" % (TestApi.host, '/api/flow', '3e6effcf99e642569b0c12b27c457ecf'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def estDeleteWorkFlow(self):
        print u'测试删除流程'
        rep = requests.delete("%s%s" % (TestApi.host, '/api/flow'), data={'id':TestApi.flowId})
        self.assertEqual(rep.status_code, 200)
        obj = json.loads(rep.content)
        self.assertTrue('code' in obj)
        self.assertEqual(obj['code'], 0)

    def testGetModuleList(self):
        print u'测试获取模块列表'
        rep = requests.get("%s%s" % (TestApi.host, '/api/module'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def testGetModuleDetail(self):
        print u'测试获取模块详细信息'
        rep = requests.get("%s%s/%s" % (TestApi.host, '/api/module', 'id'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')


