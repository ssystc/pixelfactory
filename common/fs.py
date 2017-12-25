# coding: utf-8

from const import ErrorCode
import const
import config
import os
import json
import subprocess
import webos
import flask
import model
import traceback
from common.userserver import getTokenByuserid


def createDir(fdir):
    if not os.path.exists(fdir):
        try:
            os.makedirs(fdir)
        except OSError, oe:
            config.Log.info(traceback.format_exc())

def prepareOutputDirOnWebos(userid, username, rootId,  flowObj):
    # 创建输出目录
    # def __getUsername():
    #     if 'uid' in flask.session:
    #         return model.logininfo.LoginInfoDao.getUsername(flask.session['uid'])
    #     else:
    #         return ''
    # username = __getUsername()
    token = getTokenByuserid(userid)
    outputdir = webos.createDir(userid, config.OUTPUT_DIR_NAME, rootId)
    # outputdir = webos.createDir(config.OUTPUT_DIR_NAME, rootId, classify = classify)

    # modules = flowObj.get('modules')
    # if not modules:
    #     return ErrorCode.NoModulesInFlow
    # for module in modules:
    #     name = module.get('name')
    #     if name:
    #         webos.createDir(name, outputdir, classify = classify)
    return outputdir

def prepareDirOnWebos(userid, username, rootId, flowContent):
    # 创建输入目录
    # def __getUsername():
    #     if 'uid' in flask.session:
    #         return model.logininfo.LoginInfoDao.getUsername(flask.session['uid'])
    #     else:
    #         return ''
    # username = __getUsername()
    token = getTokenByuserid(userid)
    inputdir = webos.createDir(userid, config.INPUT_DIR_NAME, rootId)
    for idir in config.INPUT_DIRS:
        webos.createDir(userid, idir, inputdir)
    prepareOutputDirOnWebos(userid, username, rootId, json.loads(flowContent))

    return ErrorCode.NoError

    # inputdir = webos.createDir(config.INPUT_DIR_NAME, rootId, classify = classify)
    # for idir in config.INPUT_DIRS:
    #     webos.createDir(idir, inputdir, classify = classify)
    #
    # prepareOutputDirOnWebos(rootId, classify, json.loads(flowContent))
    #
    # return ErrorCode.NoError


def createDirByWorkflow(rootDir, contentObj):

    createDir(rootDir)

    # 创建输入目录
    inputdir = os.path.join(rootDir, config.INPUT_DIR_NAME)
    for idir in config.INPUT_DIRS:
        createDir(os.path.join(inputdir, idir))

    # 创建输出目录和临时目录
    outputdir = os.path.join(rootDir, config.OUTPUT_DIR_NAME)
    tmpdir = os.path.join(rootDir, 'tmp')

    createDir(outputdir)
    createDir(tmpdir)

    # contentObj = json.loads(flowContent)
    # modules = contentObj.get('modules')
    # names = defaultdict(int)
    # if not modules:
    #     return ErrorCode.NoModulesInFlow
    # for module in modules:
    #     name = module.get('name')
    #     if name:
    #         dirname = name
    #         if names[name] > 0:
    #             dirname = '%s%d' % (name, names[name])
    #         createDir(os.path.join(outputdir, dirname))
    #         createDir(os.path.join(tmpdir, dirname))
    #         names[name] += 1

    return ErrorCode.NoError
