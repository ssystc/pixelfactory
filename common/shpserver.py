# coding: utf-8

import zipfile
import os
import traceback
import urllib2
import time
import config
from poster.streaminghttp import register_openers
from poster.encode import multipart_encode
import requests
import json
import uuid
from common.userserver import getTokenByuserid

def getShpExt():
    return ['.dbf', '.prj', '.shx']


def isShpPertain(fpath):
    exts = set(getShpExt())
    name, ext = os.path.splitext(fpath)
    ext = ext.lower()
    if ext in exts and os.path.exists(name + '.shp'):
        return True
    return False

def uploadShpFile(fpath, userid, productTime= str(time.time()).split('.')[0],
                  name='ssy', description='ssyupload', type='SHP', srId='4326',
                  charset='UTF-8', scale='5w'):
    config.Log.info('begin upload tiff file:%s' % fpath)
    config.Log.info('userid:%s' % userid)
    token = getTokenByuserid(userid)
    
    if not os.path.exists(fpath):
        return None
    
    try:
        filename = os.path.splitext(fpath)[0]
        layername = str(uuid.uuid4())[:5]
        dirname = os.path.dirname(filename)
        newfilename = '%s\\%s' % (dirname, layername)
        
        zfpath = '%s%s' % (newfilename, '.zip')
        
        zf = zipfile.ZipFile(zfpath, 'w')
        zf.write(fpath, ('%s.shp' % layername))
        
        for fext in getShpExt():
            fname = '%s%s' % (filename, fext)
            if os.path.exists(fname):
                zf.write(fname, ('%s%s' % (layername, fext)))
        zf.close()

        f = open(zfpath, 'rb')
        rep = requests.post('http://%s%s' % (config.SHP_SERVER_HOST, config.SHP_SERVER_UPLOAD_URL),data={
            'name': name,
            'description': description,
            'productTime': productTime,
            'type': type,
            'srId': srId,
            'charset': charset,
            'scale': scale,
            'token': token
        }, files={'file': f})
        message = json.loads(rep.content)
        return message['metadataId']
    except:
        config.Log.info(traceback.format_exc())
        config.Log.info('upload shpfile: %s error' % fpath)
        return None
    finally:
        if zf:
            zf.close()
        if zfpath and os.path.exists(zfpath):
            f.close()
            os.remove(zfpath)
            
def _getQueryParamsByMetedataId(metedataid, userid):
    token = getTokenByuserid(userid)
    rep = requests.post('http://%s%s' % (config.METEDATA_HSOT, config.METEDATA_QUERY_BY_METAID),
                        data={
                            'id': metedataid,
                            'token': token
                        })
    message = json.loads(rep.content)
    queryParams = json.loads(message['queryParams'])
    uuid = str(queryParams['uuid'])[-10:]
    wkt = str(message['wkt']['wkt'])
    srid = str(message['wkt']['srid'])
    return uuid, wkt, srid


def queryWMSUrl(metedataid, userid):
    try:
        token = getTokenByuserid(userid)
        uuid, wkt, srid = _getQueryParamsByMetedataId(metedataid, userid)
        rep = requests.post('http://%s%s' % (config.SHP_SERVER_HOST, config.SHP_WMS_URL),
                            data={
                                'token': token,
                                'grouplayerUuidLast10': uuid,
                                'wkt': wkt,
                                'width': '200',
                                'height': '200',
                                'srId': srid
                            })
        return rep.content
    except:
        config.Log.info(traceback.format_exc())
        config.Log.info("can't get shp wms url, metadataid = %s" % metedataid)
        return None


