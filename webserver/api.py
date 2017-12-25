# coding: utf-8
 
from webserver import app
import flask
import json
from model.workflow import WorkFlowDao, WorkFlow
from model.task import TaskDao, Task
from model.uidata import UiData, UiDataDao
from model.module import Module, ModuleDao
from model.taskstate import TaskState, TaskStateDao
from model.stateclan import StateClan, StateClanDao
from common.const import ErrorCode, TaskMessageField, TaskRequestType
from common import zmqutil, fs, llts, webos, dataserver
from user import login_required, getUserId
import traceback
import config
import os
from model.logininfo import LoginInfo, LoginInfoDao
from common.userserver import getTokenByuserid
import time
import logging


def _requestTaskServer(id, type, content):
    try:
        sock = zmqutil.CreateReq()
        return zmqutil.SendAndRecv(sock, {
            TaskMessageField.Type: type,
            TaskMessageField.Id: id,
            TaskMessageField.Content: content or '',
            TaskMessageField.UserUid: 'aaaaa' if config.DEBUG_STATUS else flask.session['uid']
        })
    except:
        app.logger.error(traceback.format_exc())
        app.logger.error('send msg to taskserver error')
        raise

def _requestTaskServerRetCode(id, type, content = None):
    try:
        ret = _requestTaskServer(id, type, content)
        return flask.jsonify({'code': ret[TaskMessageField.ErrCode]})
    except:
        return flask.jsonify({'code': ErrorCode.ExceptionError})


def _replaceWithModuleName(messges,modules):
    out = {}
    for key, value in messges.items():
        for module in modules:
            m = module['id']
            index = m.index('-')
            if(key[:index] == m[:index]):
                name = '%s(%s)' % (module['name'] , key[index:])
             #   temp = value.split('-')
             #   temp = temp[-1]
             #   num = int(temp)
                out[key] = name

    return out

def _getAnalysisInfo(info, names):
    test = {}
    path = None
    dic = json.loads(info.clan)
    dic = dic['__CLAN__']
    isInfo = False
    for key, value in dic.items():
        s = ''
        status = ''
        timestr = ''
        if value.has_key('inputFile') == True:
            filename = value['inputFile']
            if not path:
                path = os.path.dirname(os.path.dirname(filename))
            temp = {}
            # temp['__EXIT_CODE__'] = value['__EXIT_CODE__']
            if os.path.exists(filename):
                jsondata = json.load(open(filename, 'r'))
                if jsondata:
                    test['__ALGORITHM_CODE__'] = jsondata['Userproperty']['OutputParameter']['ProgramStatus'][0]['value']
                    test['__ALGORITHM_ANALYSE__'] = jsondata['Userproperty']['OutputParameter']['ProgramStatus'][1]['value']
                    status = test['__ALGORITHM_ANALYSE__']
                    # print 'stauts %s' % status
            else:
                status = value['__STATUS__']

            if info.starttime:
                if info.endtime:
                    timestr = u'起始时间: %s - 结束时间: %s' % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.starttime)),
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.endtime)))
                else:
                    timestr = u'起始时间: %s - 结束时间: %s' % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.starttime)),
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

            s = u'%s: %s - 状态: %s\n输入文件: %s\n' % (names[info.name], timestr, status, filename)
            temp[key] = {'__REPORT_LOG__': s}  # value

            test['__CLAN__'] = temp
            isInfo = True
            break

    strr = json.dumps(test) if isInfo == True else info.clan

    return strr

    
@app.route('/api/getEdition', methods=['GET'])
@login_required
def getEdition():
    edition = config.VERSION
    return jsonify({'edition':edition})
    
@app.route('/api/module', methods=['GET'])
@login_required
def getModuleList():
    modules = llts.getModuleList()
    modules.extend(ModuleDao.modulesList())
    return flask.jsonify(modules)

@app.route('/api/module/<id>', methods=['GET'])
@login_required
def getModuleDetail(id):
    module = llts.getToolDetail(id) or ModuleDao.queryModule(id)
    return flask.jsonify(module)

@app.route('/api/flow', methods=['GET'])
@login_required
def getWorkFlowList():
    # config.Log.info('userid = %s' % getUserId())
    wfs = [wf.dumpInfo() for wf in WorkFlowDao.workflowList(getUserId())]
    return flask.jsonify(wfs)

@app.route('/api/flow/query/<key>', methods=['GET'])
@login_required
def getWorkFlowListByKey(key):
    wfs = [wf.dumpInfo() for wf in WorkFlowDao.queryByKey(key, getUserId())]
    return flask.jsonify(wfs)

@app.route('/api/flow/getmutualflow', methods=['GET'])
@login_required
def getMutualFlow():
    wfs = [wf.dumpInfo() for wf in WorkFlowDao.getMutualFlowList()]
    return flask.jsonify(wfs)

@app.route('/api/flow/socialization', methods=['POST'])
@login_required
def flowSocializationById():
    # 流程所有者将流程公有化（所有用户可见但只有所有者可修改、删除）
    flowId = flask.request.form.get('id')
    if not flowId:
        return flask.jsonify({
            'code': ErrorCode.NoFlowIdInReq
        })
    flow = WorkFlowDao.queryWorkflow(flowId, getUserId())
    
    if flow:
        flow.type = 'mutual'
        WorkFlowDao.saveWorkflow(flow)
        return flask.jsonify({
            'code': ErrorCode.NoError,
            'flowId': flowId
        })
    else:
        return flask.jsonify({
            'code': ErrorCode.NotFindFlowById,
            'flowId': flowId
        })
    

@app.route('/api/flow/<id>', methods=['GET'])
@login_required
def getWorkFlow(id):
    wf = WorkFlowDao.queryWorkflow(id, getUserId())
    return flask.jsonify(wf.dumpDetail() if wf else {})

@app.route('/api/flow', methods=['POST'])
@login_required
def saveWorkFlow():
    # 添加流程
    flow = flask.request.form.get('content')
    if not flow:
        return flask.jsonify({
            'code': ErrorCode.NoContentInReq,
            'id': -1
        })

    flowId = flask.request.form.get('id')
    code = ErrorCode.NoError
    if flowId:
        code = WorkFlowDao.updateWorkflow(flowId, flow, getUserId())
    else:
        wf = WorkFlow(flow, getUserId())
        code = WorkFlowDao.saveWorkflow(wf)
        flowId = wf.id

    uiData = flask.request.form.get('uidata')
    if uiData:
        code = UiDataDao.setData(flowId, uiData, getUserId())

    return flask.jsonify({
        'code': code,
        'id': flowId
    })


@app.route('/api/flow', methods=['DELETE'])
@login_required
def delWorkFlow():
    userId = getUserId()
    # 删除流程
    flowId = flask.request.form.get('id')
    if not flowId:
        return flask.jsonify({'code': ErrorCode.NoFlowIdInReq})
    
    flow = WorkFlowDao.queryWorkflow(flowId, userId)
    if flow.userId != userId:
        return flask.jsonify({'code': ErrorCode.CannotDeleteMutualFlow})
    
    UiDataDao.deleteUiDataByFlowId(flowId, userId)
    taskIdList = TaskDao.queryTaskIdByFlowId(flowId, userId)
    for id in taskIdList:
        TaskStateDao.deleteTaskState(id, userId)
    TaskDao.deleteByFlowId(flowId, userId)
    code = WorkFlowDao.deleteWorkflow(flowId, userId)
    return flask.jsonify({'code': code})



@app.route('/api/task', methods=['GET'])
@login_required
def taskList():
    flowId = flask.request.args.get('flowId')
    if not flowId:
        return flask.jsonify({'code': ErrorCode.NoFlowIdInReq})
    tasks = [task.dumpInfo() for task in TaskDao.taskList(getUserId(), flowId)]
    return flask.jsonify(tasks)

@app.route('/api/task/<id>', methods=['GET'])
@login_required
def taskDetail(id):
    task = TaskDao.queryTask(id, getUserId())
    taskObj = task.dumpDetail() if task else {}
    return flask.jsonify(taskObj)

@app.route('/api/task', methods=['POST'])
@login_required
def addTask():
    content = flask.request.form.get('content')
    if not content:
        return flask.jsonify({
            'code': ErrorCode.NoContentInReq,
            'id': -1
        })
    
    taskId = flask.request.form.get('id')
    code = ErrorCode.NoError
    if taskId:
        code = TaskDao.updateTask(taskId, content, getUserId())
    else:
        task = Task(content, getUserId())
        code = TaskDao.saveTask(task)
        taskId = task.id
    return flask.jsonify({
        'code': code,
        'id': taskId
    })

        
@app.route('/api/task', methods=['DELETE'])
@login_required
def deleteTask():
    taskId = flask.request.form.get('id')
    if not taskId:
        return flask.jsonify({'code': ErrorCode.NoTaskIdInReq})
    try:
        _requestTaskServerRetCode(taskId, TaskRequestType.StopTask)
    except:
        config.Log.info('can not kill module')
    
    TaskStateDao.deleteTaskState(taskId, getUserId())
    code = TaskDao.deleteTask(taskId, getUserId())

    try:
        lltsIdList = StateClanDao.delByTaskId(taskId, getUserId())
    except:
        config.Log.info('can not kill module while delete task')
    return flask.jsonify({'code': code})



@app.route('/api/task/start', methods=['POST'])
def startTask():
    taskId = flask.request.form.get('id')
    if not taskId:
        return flask.jsonify({'code': ErrorCode.NoTaskIdInReq})

    userId = getUserId()
    # userId = '200010035103900'

    task = TaskDao.queryTask(taskId, userId)
    if not task:
        return flask.jsonify({'code': ErrorCode.NotFindTaskById})

    flow = WorkFlowDao.queryWorkflow(task.flowId, userId)
    if not flow:
        return flask.jsonify({'code': ErrorCode.NotFindFlowById})

    return _requestTaskServerRetCode(taskId, TaskRequestType.StartTask, {
        'task': task.dumpDetail(),
        'flow': flow.dumpDetail()
    })

@app.route('/api/task/pause', methods=['POST'])
@login_required
def pauseTask():
    taskId = flask.request.form.get('id')
    if not taskId:
        return flask.jsonify({'code': ErrorCode.NoTaskIdInReq})
    return _requestTaskServerRetCode(taskId, TaskRequestType.PauseTask)

@app.route('/api/task/contine', methods=['POST'])
@login_required
def contineTask():
    taskId = flask.request.form.get('id')
    if not taskId:
        return flask.jsonify({'code': ErrorCode.NoTaskIdInReq})
    return _requestTaskServerRetCode(taskId, TaskRequestType.ContinueTask)

@app.route('/api/task/stop', methods=['POST'])
@login_required
def stopTask():
    taskId = flask.request.form.get('id')
    if not taskId:
        return flask.jsonify({'code': ErrorCode.NoTaskIdInReq})
    return _requestTaskServerRetCode(taskId, TaskRequestType.StopTask)

@app.route('/api/task/state/<id>', methods=['GET'])
@login_required
def getTaskState(id):
    taskstate = TaskStateDao.lastTaskState(id, getUserId())
    if taskstate:
        clan = json.loads(taskstate.clan)
        if taskstate.endTime:
            runtime = taskstate.endTime - taskstate.startTime
        else:
            runtime = time.time() - taskstate.startTime
        clan['runTime'] = runtime
        return flask.jsonify(clan)
    else:
        return flask.jsonify({})
    # return flask.jsonify(json.loads(taskstate.clan) if taskstate else {})

@app.route('/api/fs/dir/prepare', methods=['POST'])
def prepareDir():
    flowId = flask.request.form.get('flowId')
    rootDir = flask.request.form.get('dir')
    classify = flask.request.form.get('classify', config.DEFAULT_RES_CLASSIFY)

    userid = getUserId()
      
    try:
        username = LoginInfoDao.queryUsernameByuserid(userid)
    except:
        config.Log.info(traceback.format_exc())

    code = ErrorCode.NoError
    if not flowId:
        code = ErrorCode.NoFlowIdInReq
    elif not rootDir:
        code = ErrorCode.NoDirInReq
    elif not userid:
        code = ErrorCode.NotFindUser
    else:
        flow = WorkFlowDao.queryWorkflow(flowId, getUserId())
        if not flow:
            code = ErrorCode.NotFindFlowById
        else:
            code = fs.prepareDirOnWebos(userid, username, rootDir, flow.content)

    return flask.jsonify({'code':code})

@app.route('/api/fs/list/<id>', methods=['GET'])
@login_required
def dirLists(id):
    userid = getUserId()
    if not userid:
        return flask.jsonify({'code': ErrorCode.NotFindUser})
    return flask.jsonify(webos.listTaskDir(userid, id, userid))


@app.route('/api/fs/listioput/<id>', methods=['GET'])
@login_required
def getIOputMsg(id):
    userid = getUserId()
    if not userid:
        return flask.jsonify({'code': ErrorCode.NotFindUser})
    return flask.jsonify(webos.listInputOutputDir(userid, id, userid))


@app.route('/api/fs/listbydirid/<id>')
@login_required
def getListByDirId(id):
    userid = getUserId()
    if not userid:
        return flask.jsonify({'code': ErrorCode.NotFindUser})
    return flask.jsonify(webos.listDirByDirId(userid, id))



@app.route('/api/fs/listinput', methods=['POST'])
@login_required
def listInputDirByDirid():
    userid = getUserId()
    if not userid:
        return flask.jsonify({'code': ErrorCode.NotFindUser})

    dirid = int(flask.request.form['dirid'])

    def _listdir(dirid):
        dirs = webos.listDir(userid, dirid)

        for d in dirs:
            if d['type'] == 'dir' and 'output' not in d['path'] :
                d['children'] = _listdir(d['id'])
        return dirs
    try:
        message = flask.jsonify(_listdir(dirid))
        return message
    except:
        config.Log.info('list Input error')



@app.route('/api/fs/list', methods=['POST'])
@login_required
def listDirByDirid():

    userid = getUserId()
    if not userid:
        return flask.jsonify({'code': ErrorCode.NotFindUser})
    dirid = int(flask.request.form['dirid'])

    def _listdir(dirid):
        dirs = webos.listDir(userid, dirid)
        for d in dirs:        
            if d['type'] == 'dir':
                d['children'] = _listdir(d['id'])
        return dirs
    try:
        message = flask.jsonify(_listdir(dirid))
        return message
    except:
        config.Log.info('list Dir Error')


@app.route('/api/flow/ui/data/<id>', methods=['GET'])
@login_required
def getFlowUiData(id):
    return UiDataDao.getData(id, getUserId())

@app.route('/api/flow/ui/data', methods=['POST'])
@login_required
def setFlowUiData():
    flowId = flask.request.form.get('flowId')
    content = flask.request.form.get('content')
    code = ErrorCode.NoError
    if not flowId:
        code = ErrorCode.NoFlowIdInReq
    elif not content:
        code = ErrorCode.NoContentInReq
    else:
        code = UiDataDao.setData(flowId, content, getUserId())
    return flask.jsonify({'code': code})

@app.route('/', methods=['GET'])
def homepage():
    return flask.redirect(config.INDEX_PAGE)


@app.route('/api/stateclan/query', methods=['POST'])
@login_required
def queryStateclan():
    userid = getUserId()
    taskid = flask.request.form.get('taskid')
    if not taskid:
        code = ErrorCode.NoTaskIdInReq
        return flask.jsonify({'code': code})

    stateclanList = StateClanDao.queryByTaskId(taskid, userid)
    if not stateclanList:
        code = ErrorCode.NotFindStateClanByTask
        return flask.jsonify({'code': code})

    message = {}

    modules = llts.getModuleList()

    names = {}
    for it in stateclanList:
        names[it.name] = it.name

    names = _replaceWithModuleName(names, modules)

    for info in stateclanList:

        strr = _getAnalysisInfo(info, names)

        if info.starttime:
            if info.endtime:
                message[names[info.name]] = {'clan': strr, 'runtime': info.endtime - info.starttime}
            else:
                message[names[info.name]] = {'clan': strr, 'runtime': time.time() - info.starttime}
        else:
            message[names[info.name]] = {'clan': strr, 'runtime': 0.0}

    return flask.jsonify(message)
'''
def queryStateclan():
    userid = getUserId()
    taskid = flask.request.form.get('taskid')
    if not taskid:
        code = ErrorCode.NoTaskIdInReq
        return flask.jsonify({'code': code})

    stateclanList = StateClanDao.queryByTaskId(taskid, userid)
    if not stateclanList:
        code = ErrorCode.NotFindStateClanByTask
        return flask.jsonify({'code': code})

    message = {}
    for info in stateclanList:
        if info.starttime:
            if info.endtime:
                message[info.name] = {'clan': info.clan, 'runtime': info.endtime - info.starttime}
            else:
                message[info.name] = {'clan': info.clan, 'runtime': time.time() - info.starttime}
        else:
            message[info.name] = {'clan': info.clan, 'runtime': 0.0}
    return flask.jsonify(message)
'''

@app.route('/api/taskstatus/query', methods=['POST'])
@login_required
def queryTaskStatus():
    userid = getUserId()
    flowid = flask.request.form.get('flowid')
    if not flowid:
        code = ErrorCode.NoFlowIdInReq
        return flask.jsonify({'code': code})

    taskIdList = TaskDao.queryTaskIdByFlowId(flowid, userid)
    if taskIdList == []:
        code = ErrorCode.NotFindTaskByFlowId
        return flask.jsonify({'code': code})

    taskstateList = []
    message = {}

    for taskid in taskIdList:
        taskstate = TaskStateDao.lastTaskState(taskid, userid)
        if taskstate:
            taskstateList.append(taskstate)
        else:
            message[taskid] = 'NotRuning'

    for info in taskstateList:
        if info.endTime:
            message[info.taskId] = 'NotRuning'
        else:
            message[info.taskId] = 'Runing'

    return flask.jsonify(message)


@app.route('/api/task/querybyargs', methods=['POST'])
@login_required
def queryTaskStateByArgs():
    userid = getUserId()
    sortName = flask.request.form.get('sortName')
    sortOrder = flask.request.form.get('sortOrder')
    pageSize = flask.request.form.get('pageSize')
    pageNumber = flask.request.form.get('pageNumber')
    
    config.Log.info('sortname = %s, sortorder = %s, pageSize = %s, pagenumber = %s, userid = %s' % (sortName, sortOrder, pageSize, pageNumber, userid))
    
    taskstatelist = TaskStateDao.queryByArgs(sortName, sortOrder, pageSize, pageNumber, userid)
    states = {}
    states['rows'] = [taskstate.dumpDetail() for taskstate in taskstatelist]
    states['total'] = TaskStateDao.queryCount(userid)
    return flask.jsonify(states)
    


