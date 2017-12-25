# coding: utf-8

import requests
import json
import config
import traceback
from error import MsgException
from const import ErrorCode
import os
from common.userserver import getTokenByuserid

def downloadFile(dataid, saveToPath, token=u'testuser'):
    try:
        url = 'http://%s%s' % (config.DATA_SERVER_HOST, config.DATA_SERVER_DOWNLOAD_URL)
        rep = requests.post(url, data = {
            'id': dataid,
            'token': token
        })
        if rep.status_code != 200:
            config.Log.info('failed download file (%s:%s)' % (saveToPath, dataid))
            return
        obj = rep.content
        if 'errors_code' in obj:
            raise MsgException(ErrorCode.DownloadFaild, u'download file faild. fileid = %s' % dataid)

        with open(saveToPath, 'wb') as f:
            for data in rep.iter_content(chunk_size = 1024):
                f.write(data)
        # config.Log.info('download file success (%s:%s)' % (saveToPath, dataid))
    except:
        # config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.DownloadFaild, u'download file faild. fileid = %s' % dataid)

def uploadFile(fpath, longitude="0.0", latitude="0.0", token="testuser"):
    config.Log.info('begin upload file: %s' % fpath)
    fsize = os.path.getsize(fpath)
    if fsize > config.DATA_FILE_SIZE_LIMIT:
        config.Log.info('%s is big file size :%.2fM' % (fpath, fsize/1024/1024))
        return None 
 
    url = 'http://%s%s' % (config.DATA_SERVER_HOST, config.DATA_SERVER_UPLOAD_URL)
    
    try:
        rep = requests.post(url, data={
            "longitude": longitude,
            "latitude": latitude,
            "token": token
        }, files={"file": open(fpath, 'rb')})
        dic = json.loads(rep.content)
        return dic['result']['id']
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.UploadFileFaild, u'upload load file faild. path = %s' % fpath)

def getPreviewUrl(dataid):
    return '%s%s?id=%s' % (config.DATA_SERVER_HOST, config.DATA_SERVER_DOWNLOAD_URL, dataid)


def uploadModuleJson(taskId, folderId, jsonFileDir, userid, state):
    token = getTokenByuserid(userid)
    jsonFiles = json.load(open(jsonFileDir), encoding='utf-8')
    jsonFiles = json.dumps(jsonFiles)
    rep = requests.post('http://%s%s' % (config.EP_HOST, config.EP_UPLOAD_MODULEJSON_URL),data=json.dumps({
        'taskId': taskId,
        'folderId': folderId,
        'jsonFiles': jsonFiles,
        'token': token,
        'state': state
    }, ensure_ascii=False))
    message = json.loads(rep.content)
    return message['status']
    
    
