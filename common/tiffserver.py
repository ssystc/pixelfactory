# coding: utf-8

import urllib2
from poster.streaminghttp import register_openers
from poster.encode import multipart_encode
import json
import config
import os
import subprocess
from error import MsgException
import traceback
from const import ErrorCode
import requests
from userserver import getTokenByuserid, refreshToken


def querySliceUrl(token):
    try:
        rep = requests.get('http://%s%s/?token=%s' % (config.TIFF_DATA_HOST, config.TIFF_QUERY_SLICE_URL, token))
        return rep.content    
    except:
        config.Log.info()


def queryData(metadataid, userid):
    try:
        token = getTokenByuserid(userid)
        config.Log.info('metadataid = %s , token = %s' % (metadataid, token))
        rep = requests.post('http://%s%s' % (config.METEDATA_HSOT, config.METEDATA_QUERY_BY_METAID),
                            data={
                                'id': metadataid,
                                'token': token
                            })
	
	
        message = json.loads(rep.content)
        imageId = json.loads(message['queryParams'])['id']

        nextrep = requests.post('http://%s%s' % (config.TIFF_DATA_HOST, config.TIFF_DATA_QUERY_BY_TIFFID),
                                data={
                                    'id': imageId,
                                    'token': token
                                })
        nextmessage = nextrep.content
        return nextmessage
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.FindTiffDataError, u'get tiff data information error')


def queryPngLayerName(metadataid, userid):
    message = json.loads(queryData(metadataid, userid))
    message = message['sliceTasks']
    # config.Log.info('########################%s' % metadataid)
    # config.Log.info('########################%s' % message)
    if message:
        for info in message:
            if info['mimeType'] == 'png':
                return info['layerName']

    else:
        config.Log.info("can't get metadata information or info has no layername attribute, metadataid = %s" % metadataid)
        return None


def queryTiffLayerName(metadataid, userid):
    message = json.loads(queryData(metadataid, userid))
    message = message['sliceTasks']
    if message:
        for info in message:
            if info['mimeType'] == 'tif':
                return info['layerName']

    else:
        config.Log.info(
            "can't get metadata information or info has no layername attribute, metadataid = %s" % metadataid)
        return None

def queryProductLayerName(metadataid, userid):
    try:
        message = json.loads(queryData(metadataid, userid))
        message = message['sliceTasks']
        if message:
            for info in message:
                if info['mimeType'] == 'product':
                    return info['layerName']

        else:
            config.Log.info("can't get metadata information or info has no layername attribute, metadataid = %s" % metadataid)
            return None
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.FindTiffDataError, u'get tiff layername error: %s' % traceback.format_exc())



def queryWMSUrl(metadataid, userid):
    try:
        message = {}
        
        data = queryData(metadataid,userid)
        obj = json.loads(data)
        
        sliceTasks = obj['sliceTasks']
        for task in sliceTasks:
            if task['mimeType'] == 'png':
                tilestatus = task['tileStatus']
                if tilestatus != 'DONE':
                    message['status'] = tilestatus
                    return message
      
        layerName = queryPngLayerName(metadataid, userid)
        tllon = obj['upleftLon']
        tllat = obj['upleftLat']
        brlon = obj['lowrightLon']
        brlat = obj['lowrightLat']
        url = 'http://%s%s%s&bbox=%f,%f,%f,%f' % (config.IMG_SERVER_HOST, config.IMG_SERVER_WMS_URL, layerName, tllon, tllat, brlon, brlat)
        message['status'] = 'DONE'
        message['message'] = url
        return message
    except:
        config.Log.info("can't get layer wms url, metadataid = %s" % metadataid)
        return 'SLICE TASK ERROR'


def queryDataUrl(metadataid, userid):
    layerName = queryProductLayerName(metadataid, userid)
    if layerName:
        return 'info="http://%s%s%s",data="http://%s%s%s"' % (config.IMG_SERVER_HOST, config.IMG_SERVER_INFO_URL, layerName, config.IMG_SERVER_HOST, config.IMG_SERVER_DATA_URL, layerName)
    else:
        return None


def uploadTiffFile(fpath, mimetypes, userid, keyword, dataType='0201'):
    config.Log.info('begin upload tiff file: %s' % fpath)

    def _transSpimgToTiff(fpath):
        spdatapath = fpath + '.data'
        if os.path.isdir(spdatapath):
            tiffpath = fpath + '.tiff'
            config.Log.info('convert spimg to tiff <%s:%s>' % (fpath, tiffpath))
            # subprocess.call("gdal_translate %s %s" % (fpath, tiffpath), shell=True)
            subprocess.call("bash ./common/trans/trans.sh %s %s GTiff" % (fpath, tiffpath), shell=True)
            return tiffpath
        return fpath

    try:
        token = refreshToken(userid)
        tiffpath = _transSpimgToTiff(fpath)

        register_openers()
        datagen, headers = multipart_encode({"file": open(fpath, "rb"),
                                             "imageMeta.dataType": dataType,
                                             "imageMeta.keyword": keyword,
                                             "mimeTypes": mimetypes,
                                             'token': token
                                            })

        url = 'http://%s%s' % (config.TIFF_DATA_HOST, config.TIFF_DATA_UPLOAD_URL)
        req = urllib2.Request(url, datagen, headers)

        if tiffpath != fpath:
            os.remove(tiffpath)

        message = urllib2.urlopen(req).read()
        obj = json.loads(message)

        return obj['metadataId']
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.UploadTiffFileFaild, u'upload tiff file faild. path = %s' % fpath)


def isSpimgPertian(fpath):
    if fpath.endswith('.data'):
        tifPath = fpath[0:len(fpath) - 5]
        if os.path.exists(tifPath) and os.path.isfile(tifPath):
            return True
    return False

