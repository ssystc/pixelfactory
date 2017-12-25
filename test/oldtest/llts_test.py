# coding:utf-8

import unittest
import json
import requests

class TestLLTS(unittest.TestCase):

    llts_api = 'http://192.168.44.111:9019/api/v1/llts/api'
    llts_tool_list = 'http://192.168.44.111:9019/api/v1/llts/getList'
    llts_tool_detail = 'http://192.168.44.111:9019/api/v1/llts/get/transtiff-0.0.1'

    def testGetTaskList(self):
        print u'测试 llts api接口'
        detailReq = { '__TYPE__': "TASK/DETAILS" }
        rep = requests.post(TestLLTS.llts_api, data=json.dumps(detailReq))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def testGetToolList(self):
        print u'测试获取工具列表'
        rep = requests.get(TestLLTS.llts_tool_list)
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def testGetToolDetail(self):
        print u'测试获取工具详细信息'
        rep = requests.get(TestLLTS.llts_tool_detail)
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')
