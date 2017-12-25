# coding: utf-8

import unittest
import requests
import json

class TestFs(unittest.TestCase):

    host = 'http://192.168.4.221:8083'
    rootDir = '/data/llts-data/testdata/testxxxx'

    testFlowId = '98f7b518baf7416d839c9947abda840b'
    testTaskId = 'd909f1fc5aa641999ece5600ed325400'


    def testPrepareDir(self):
        print u'测试准备目录'
        rep = requests.post('%s%s' % (TestFs.host, '/api/fs/dir/prepare'),
            data = [
                ('flowId', TestFs.testFlowId),
                ('dir', TestFs.rootDir)
            ])
        self.assertEqual(rep.status_code, 200)
        repObj = json.loads(rep.content)
        self.assertEqual(repObj.get('code'), 0)
        print rep.content.decode('utf-8')

    def testListDir(self):
        print u'测试列出目录'
        rep = requests.get('%s%s%s' % (TestFs.host, '/api/fs/list/', TestFs.testTaskId))
        self.assertEqual(rep.status_code, 200)
        repObj = json.loads(rep.content)
        self.assertEqual(repObj.get('code'), 0)
        print rep.content.decode('utf-8')

