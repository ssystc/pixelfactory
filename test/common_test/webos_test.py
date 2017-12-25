#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import mock
import unittest
from common import userserver
from model.logininfo import LoginInfo, LoginInfoDao
import config
import json
import requests
from taskserver.log import Log
from common import webos
from model.task import Task, TaskDao
from common.const import ErrorCode
from model.taskstate import TaskStateDao, TaskState
from common import tiffserver, shpserver, dataserver


class webosTest(unittest.TestCase):
    config.Log = Log
    testClan = '''
{
    "errorCode": 0,
    "fileuploading": true,
    "OC37b7a0ab-9638-4081-9119-2ced1b815261-1": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808395.05_JQqeO",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    },
    "OC37b7a0ab-9638-4081-9119-2ced1b815261-0": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808395.34_jHcQf",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    },
    "errorMessage": "",
    "RSUniformColorb465b328-e477-4d04-a914-32ddac803650-0": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808639.91_jTaMZ",
        "returnCode": 0,
        "returnMsg": "Process success.",
        "fsid": null,
        "exitCode": 0
    },
    "paused": false,
    "0dc9d7fb-150d-4922-bd90-ae068f178a1f": {
        "code": 3,
        "uploading": false,
        "detail": null,
        "returnCode": 0,
        "returnMsg": "",
        "fsid": null,
        "exitCode": 0
    },
    "state": 2,
    "RSUniformColorb465b328-e477-4d04-a914-32ddac803650-1": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808624.6_dbwev",
        "returnCode": 0,
        "returnMsg": "Process success.",
        "fsid": null,
        "exitCode": 0
    },
    "GSImageSharpenDistribut6ca0c501-9edd-40ef-875b-1c0863c3435d-1": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808455.01_ritKy",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    },
    "GSImageSharpenDistribut6ca0c501-9edd-40ef-875b-1c0863c3435d-0": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808450.3_jLYbO",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    },
    "taskId": "191c9384828a49c3abcafa9b2154226b",
    "__start_module__": {
        "code": 3,
        "uploading": false,
        "detail": null,
        "returnCode": 0,
        "returnMsg": "",
        "fsid": null,
        "exitCode": 0
    },
    "__end_module__": {
        "code": 3,
        "uploading": false,
        "detail": null,
        "returnCode": 0,
        "returnMsg": "",
        "fsid": null,
        "exitCode": 0
    },
    "OCec44884e-ac24-4130-80b1-fa3827b8682c-1": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808395.64_OZayy",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    },
    "OCec44884e-ac24-4130-80b1-fa3827b8682c-0": {
        "code": 3,
        "uploading": true,
        "detail": "TASK_1505808395.92_heThL",
        "returnCode": 0,
        "returnMsg": "SUCCESS",
        "fsid": null,
        "exitCode": 0
    }
}
    '''
    testTaskState = TaskState('testtaskid', 0, 0.0, 1.0, 2.0, testClan, '200010035342948', '200010035324693')
    testTaskJson = {
        "id": "",
        "name": "测试任务",
        "desc": "测试流程的任务",
        "owner": "ssy",
        "createDate": "2017.08.08",
        "flowId": "5070cb4a6e03464d8b4583ab069cca67",
        "dir": "/home/llts/lzz/data",
        "args": [
            {"name": "tiffFile", "title": "输入影像文件", "type": "string", "value": "", "auto": ["_transtiff.tiff"]}
        ]
    }
    testTask = Task(json.dumps(testTaskJson, ensure_ascii=False), '200010035324693')
    testListDirResult = [
        {
            'path': 'output', 'metadataid': None, 'type': 'dir', 'id': 200010035342948
        },
        {
            'path': 'output_2b14e8fbaf124d028a3d302e212e102b', 'metadataid': None, 'type': 'dir', 'id': 200010035342881
        },
        {
            'path': 'input', 'metadataid': None, 'type': 'dir', 'id': 200010035338901
        },
        {
            'path': 'testtiff.tiff', 'metadataid': 'testmetadataid', 'type': 'file', 'id': 200010035342883
        }
    ]
    testUploadFsRoot = './test/common_test/test_upload_file/output'

    
    def test_a_ListInputOutputDir(self):
        print u'*************** 测试根据taskid列出Input和Output ***************'
        
        # 根据taskId查不到task信息
        TaskDao.queryTask = mock.Mock(return_value=None)
        info = webos.listInputOutputDir('testtoken', 'testtaskid', 'testuserid')
        self.assertEqual(info['code'], ErrorCode.NotFindTaskById)
        
        # 根据taskId可以查到task信息
        TaskDao.queryTask = mock.Mock(return_value=webosTest.testTask)
        webos.listDir = mock.Mock(return_value=webosTest.testListDirResult)
        TaskStateDao.lastTaskState = mock.Mock(return_value=webosTest.testTaskState)
        obj = webos.listInputOutputDir('testtoken', 'testtaskid', 'testuserid')
        self.assertEqual(obj['code'], ErrorCode.NoError)
        
    def test_b_ListDirByDirId(self):
        print u'*************** 测试根据taskid列出文件列表 ***************'
        webos.listDir = mock.Mock(return_value=webosTest.testListDirResult)
        dataserver.getPreviewUrl = mock.Mock(return_value=None)
        shpserver.queryWMSUrl = mock.Mock(return_value=None)
        tiffserver.queryWMSUrl = mock.Mock(return_value='test tiff WMS url')
        obj = webos.listDirByDirId('testtoken', 'testdirid')
        self.assertTrue('test tiff WMS url' in json.dumps(obj))
        
    def test_c_Upload(self):
        print u'*************** 测试上传文件，并在数据库中创建相应的目录结构 ***************'
        
        webos.listDir = mock.Mock(return_value=webosTest.testListDirResult)
        webos.createDir = mock.Mock(return_value='testDirId')
        webos.createFile = mock.Mock(return_value='testFileId')
        tiffserver.uploadTiffFile = mock.Mock(return_value='testTiffId')
        shpserver.uploadShpFile = mock.Mock(return_value='testShpId')
        dataserver.uploadFile = mock.Mock(return_value='testDataId')
        info = webos.uploadDir('testtoken', 'testdirid', 'testusername', webosTest.testUploadFsRoot)
        self.assertEqual(info, 200010035342948)
        
if __name__ == '__main__':
    unittest.main()


