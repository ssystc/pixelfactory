# coding: utf-8

import config
import json
import os
import tiffserver
import dataserver
import shpserver
from const import ErrorCode
from error import MsgException
from model.task import TaskDao, Task
from model.taskstate import TaskStateDao, TaskState
from model.logininfo import LoginInfoDao, LoginInfo
import traceback
import requests
import flask
import flask.sessions
import model.logininfo
import M2Crypto
import base64
from common.userserver import getTokenByuserid


class FileType(object):
    NORMAL_FILE = 0,
    TIFF_FILE = 1,
    SHP_FILE = 2

def checkFileType(fpath):
    ext = os.path.splitext(fpath)[-1].lower()
    if ext == '.tif' or ext == '.tiff':
        return FileType.TIFF_FILE
    elif ext == '.shp':
        return FileType.SHP_FILE
    else:
        return FileType.NORMAL_FILE


# 在webos上创建目录
def createDir(userid, filename, parentId, type = '1', edittype = 0):
    try:
        token = getTokenByuserid(userid)
        url = 'http://%s%s' % (config.WEBOS_DIR_HOST, config.WEBOS_MKDIR_URL)
        rep = requests.post(url, {
            'token': token,
            'filemanager.Name': filename,
            'filemanager.ParentID': parentId,
            'filemanager.Type': type,
            'filemanager.editType': edittype
        })
        obj = json.loads(rep.content)
        return obj['item']['items'][0]['id']
    except:
        config.Log.info('parentId = %s, token = %s, filename = %s' % (parentId, token, filename))
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.CreateDirOnWebosFaild, u'create dir on webos failed.')


# 在目录中创建文件
def createFile(userid, filename, parentId, metadataId, datatype, type = '0', edittype = 0):
    try:
        token = getTokenByuserid(userid)
        url = 'http://%s%s' % (config.WEBOS_DIR_HOST, config.WEBOS_MKDIR_URL)
        rep = requests.post(url, {
            'token': token,
            'filemanager.Name': filename,
            'filemanager.ParentID': parentId,
            'filemanager.Metadata': metadataId,
            'filemanager.dataType': datatype,
            'filemanager.Type': type,
            'filemanager.editType': edittype
        })
        obj = json.loads(rep.content)
        return obj['item']['items'][0]['id']
    except:
        config.Log.info('parentId = %s, token = %s, filename = %s' % (parentId, token, filename))
        config.Log.info(rep.content)
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.CreateDirOnWebosFaild, u'create dir on webos failed.')

def removeDir(userid, dirid):
    try:
        token = getTokenByuserid(userid)
        url = 'http://%s%s' % (config.WEBOS_DIR_HOST, config.WEBOS_REMOVEDIR_URL)
        rep = requests.post(url,
                            data={
                                'token': token,
                                'ids': dirid
                            })
    except:
        config.Log.info('dirid = %s' % dirid)
        config.Log.info(traceback.format_exc())

def rename(userid, scjId, newParentId, newName):
    try:
        token = getTokenByuserid(userid)
        url = 'http://%s%s' % (config.WEBOS_DIR_HOST, config.WEBOS_EDITOR_URL)
        rep = requests.post(url, {
            'token': token,
            'filemanager.id': scjId,
            'filemanager.ParentID': newParentId,
            'filemanager.Name': newName
        })
        config.Log.info('rename output dir to %s . rep = %s' % (newName, rep.content))
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.RenameDirOnWebosFaild, u'rename dir on webos failed.')



def listDir(userid, dirId):
    try:
        config.Log.info('goto getFavinfoByParentId: parentId=%s' % dirId)
        token = getTokenByuserid(userid)
        config.Log.info('goto getFavinfoByParentId: userid = %s, parentId=%s, token = %s' % (userid, dirId, token))
        url = 'http://%s%s' % (config.WEBOS_DIR_HOST, config.WEBOS_LISTDIR_URL)
        rep = requests.post(url, {
            'token': token,
            'parentId':dirId
        })
        
        obj = json.loads(rep.content)
        

        def _isDir(item):
            return item.get('type') == '1'

        return [{
            'id': item.get('id'),
            'path': item.get('name'),
            'type': 'dir' if _isDir(item) else 'file',
            'metadataid': item.get('metadata')
        } for item in obj['item']['items'] or []]
    except:
        config.Log.info('###################token = %s, dirId = %s##############' % (token, dirId))
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.ListDirError, u"get dir list error.")




# 查看resName是否在某个文件夹中
def findResource(userid, parentId, resName):
    token = getTokenByuserid(userid)
    for d in listDir(token, parentId):
        if d['path'] == resName:
            return d
    return None


# 上传文件，并在李垚数据库中创建相应的目录结构
def uploadDir(userid, dirId, fsRoot, tiffkeyword='ProductImage_iFactory'):
	
    config.Log.info('begin goto uploadDir method')

    
    def __uploadDir(dirid, fs):
        config.Log.info('__uploadDir(%s,%s)' % (dirid, fs))
        osdirs = {}
        for d in listDir(userid, dirid):
            osdirs[d['path']] = d

        config.Log.info('local files: %s' % os.listdir(fs))

        for d in os.listdir(fs):
            if os.path.isdir(os.path.join(fs, d)):
                if tiffserver.isSpimgPertian(os.path.join(fs, d)):
                    continue
                if d in osdirs and osdirs[d]['type'] == 'dir':
                    subid = osdirs[d]['id']
                    __uploadDir(subid, os.path.join(fs, d))
                else:
                    subid = createDir(userid, d, dirid)
                    __uploadDir(subid, os.path.join(fs, d))
            else:
                if d not in osdirs or osdirs[d]['type'] != 'file':
			
                    config.Log.info('************dir msg: %s***********' % d)

                    if shpserver.isShpPertain(os.path.join(fs, d)):
                        continue
                    ft = checkFileType(d)
                    metadataid = None
                    if ft == FileType.TIFF_FILE:
                        config.Log.info('************tiff path: %s*************' % os.path.join(fs, d))
                        metadataid = tiffserver.uploadTiffFile(os.path.join(fs, d), json.dumps(['png', 'product']), userid, tiffkeyword)
                        datatype = u'局部影像'
                    elif ft == FileType.SHP_FILE:
                        metadataid = shpserver.uploadShpFile(os.path.join(fs, d), userid)
                        datatype = u'局部矢量'
                    else:
                        metadataid = dataserver.uploadFile(os.path.join(fs, d), token = 'testuser')
                        datatype = u'文档'
                    if metadataid:
                        createFile(userid, d, dirid, metadataid, datatype)
    
    osdirs = {}
    for d in listDir(userid, dirId):
        osdirs[d['path']] = d

    subdirid = None
    dirname = os.path.basename(fsRoot)
    if dirname in osdirs:
        subdirid = osdirs[dirname]['id']
    else:
        subdirid = createDir(userid, dirname, dirId)

    __uploadDir(subdirid, fsRoot)
    return subdirid

#
# def uploadDir(dirId, userId, fsRoot, classify = config.DEFAULT_RES_CLASSIFY):
#
#     def __uploadDir(dirid, fs):
#         osdirs = {}
#         for d in listDir(dirid, classify):
#             osdirs[d['path']] = d
#
#         for d in os.listdir(fs):
#             if os.path.isdir(os.path.join(fs, d)):
#                 if tiffserver.isSpimgPertian(os.path.join(fs, d)):
#                     continue
#                 if d in osdirs and osdirs[d]['type'] == 'dir':
#                     subid = osdirs[d]['id']
#                     __uploadDir(subid, os.path.join(fs, d))
#                 else:
#                     subid = createDir(d, dirid, classify=classify)
#                     __uploadDir(subid, os.path.join(fs, d))
#             else:
#                 if d not in osdirs or osdirs[d]['type'] != 'file':
#                     if shpserver.isShpPertain(os.path.join(fs, d)):
#                         continue
#                     ft = checkFileType(d)
#                     dataid = None
#                     if ft == FileType.TIFF_FILE:
#                         dataid = tiffserver.uploadTiffFile(os.path.join(fs, d))
#                     elif ft == FileType.SHP_FILE:
#                         dataid = shpserver.uploadShpFile(os.path.join(fs, d))
#                     else:
#                         dataid = dataserver.uploadFile(os.path.join(fs, d), token = userId)
#
#                     if dataid:
#                         createFile(dataid, d, dirid, classify=classify)
#
#     osdirs = {}
#     for d in listDir(dirId, classify):
#         osdirs[d['path']] = d
#
#     subdirid = None
#     dirname = os.path.basename(fsRoot)
#     if dirname in osdirs:
#         subdirid = osdirs[dirname]['id']
#     else:
#         subdirid = createDir(dirname, dirId, classify = classify)
#
#     __uploadDir(subdirid, fsRoot)
#
#     return subdirid


def listTaskDir(userid, taskId, userId):
    task = TaskDao.queryTask(taskId, userId)
    if not task:
        return {'code': ErrorCode.NotFindTaskById}
    token = getTokenByuserid(userid)
    def _listDir(dirid):
        ret = []
        dirs = listDir(token, dirid)
        for d in dirs:
            if d['type'] == 'dir':
                ret.append({
                    'type': 'dir',
                    'path': d['path'],
                    'children': _listDir(d['id'])
                })
            elif d['type'] == 'file':
                obj = {'type': 'file', 'path': d['path']}
                ft = checkFileType(d['path'])
                if ft == FileType.TIFF_FILE:
                    obj['url'] = tiffserver.queryWMSUrl(d['metadataid'], userid)
                elif ft == FileType.SHP_FILE:
                    obj['url'] = shpserver.queryWMSUrl(d['metadataid'], userid)
                else:
                    obj['url'] = dataserver.getPreviewUrl(d['metadataid'])
                ret.append(obj)
        return ret
    
    dirs = listDir(token, task.dir)
    
    taskState = TaskStateDao.lastTaskState(taskId, userId)
    inputs = None
    outputs = None
    for d in dirs:
        if d['path'] == config.INPUT_DIR_NAME:
            inputs = _listDir(d['id'])
        elif taskState and str(d['id']) == taskState.fsId:
            outputs = _listDir(d['id'])

    return {
        'code': ErrorCode.NoError,
        'type': 'dir',
        'path': task.name,
        'children': [
            {'type': 'dir', 'path': config.INPUT_DIR_NAME, 'children': inputs or []},
            {'type': 'dir', 'path': config.OUTPUT_DIR_NAME, 'children': outputs or []}
        ]
    }


def listInputOutputDir(userid, taskId, userId):
    token = getTokenByuserid(userid)
    task = TaskDao.queryTask(taskId, userId)
    inputid = None
    outputid = None
    inputname = None
    outputname = None
    if not task:
        return {'code': ErrorCode.NotFindTaskById}
    dirs = listDir(userid, task.dir)
    taskState = TaskStateDao.lastTaskState(taskId, userId)
    for d in dirs:
        if d['path'] == config.INPUT_DIR_NAME:
            inputid = d['id']
            inputname = d['path']

        elif taskState and str(d['id']) == taskState.fsId:
            outputid =  d['id']
            outputname = d['path']
    return {
        'code': ErrorCode.NoError,
        'type': 'dir',
        'path': task.name,
        'children': [
            {'type': 'dir', 'path': inputname, 'id': inputid, 'children': []},
            {'type': 'dir', 'path': outputname, 'id': outputid, 'children': []}
        ]
    }

def listDirByDirId(userid, dirId):
    ret = []
    dirs = listDir(userid, dirId)
    for d in dirs:
        if d['type'] == 'dir':
            ret.append({
                'type': 'dir',
                'path': d['path'],
                'id': d['id'],
                'children': []
            })
        elif d['type'] == 'file':
            obj = {'type': 'file', 'path': d['path']}
            ft = checkFileType(d['path'])
            if ft == FileType.TIFF_FILE:
                obj['url'] = tiffserver.queryWMSUrl(d['metadataid'], userid)
            elif ft == FileType.SHP_FILE:
                obj['url'] = shpserver.queryWMSUrl(d['metadataid'], userid)
            else:
                obj['url'] = dataserver.getPreviewUrl(d['metadataid'])
            ret.append(obj)
    return ret



