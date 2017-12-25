# coding: utf-8

import unittest
import requests
import json


class TestTask(unittest.TestCase):

    host = 'http://localhost:8283'
    taskId = None

    def testAddTask(self):
        print u'测试添加任务'
        task = json.load(open('../task.json'))
        content = json.dumps(task, indent=4, ensure_ascii=False)
        rep = requests.post("%s%s" % (TestTask.host, '/api/task'), data=[
            ('content', content)
        ])
        self.assertEqual(rep.status_code, 200)

        obj = json.loads(rep.content)
        self.assertTrue('id' in obj and 'code' in obj)
        self.assertEqual(obj['code'], 0)

        TestTask.taskId = obj.get('id')

    def testDeleteTask(self):
        print u'测试删除任务'
        rep = requests.delete("%s%s" % (TestTask.host, '/api/task'), data=[
            ('id', TestTask.taskId)
        ])
        self.assertEqual(rep.status_code, 200)
        print rep.content


    def testGetTask(self):
        print u'测试获取任务列表（所有任务）'
        rep = requests.get("%s%s" % (TestTask.host, '/api/task'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

        print u'测试获取指定流程绑定的任务 %s' % '3e6effcf99e642569b0c12b27c457ecf'
        rep = requests.get("%s%s?flowId=%s" % (TestTask.host, '/api/task', '3e6effcf99e642569b0c12b27c457ecf'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')
    
    def testGetTaskDetail(self):
        print u'测试获取任务详情'
        rep = requests.get("%s%s/%s" % (TestTask.host, '/api/task', '1607527d6d4046b9bf89840ad31becc3'))
        self.assertEqual(rep.status_code, 200)
        print rep.content.decode('utf-8')

    def testStartTask(self):
        print u'测试启动任务'
        rep = requests.post("%s%s" % (TestTask.host, '/api/task/start'), data=[
            ('id', '42ab796d745844c182289d6faf8dcc3b')
        ])
        self.assertEqual(rep.status_code, 200)
        print rep.content



