# coding: utf-8

import config
import requests
from lltsconst import RequestField, RequestType
import json
from error import MsgException
from const import ErrorCode
import traceback

def __callLLTSApi(req):
    try:
        rep = requests.post(
            'http://%s%s' % (config.LLTS_TEMPORARY_HOST, config.LLTS_TEMPORARY_API_URL),
            data = [('request',json.dumps(req))]
        )
        return rep.content
    except:
        config.Log.info(traceback.format_exc())
        raise MsgException(ErrorCode.LLTSCallError, u'call llts error.')

def getToolDetail(toolId):
    url = 'http://%s%s' % (config.CENTER_HOST, config.LLTS_TOOL_DETAIL.format(id=toolId))
    try:
        rep = requests.get(url)
        return json.loads(rep.content)
    except:
        return {}

def getModuleList():

    def __getToolId(tooldetail):
        op = tooldetail.get('op')
        ver = tooldetail.get('version')
        return '%s-%s' % (op, ver) if ver else op

    def __getDetail(tool):
        return json.loads(tool.get('data', {}))

    def __getToolInfo(tool):
        detail = __getDetail(tool)
        return {
            'id': __getToolId(detail),
            'name': detail.get('name', ''),
            'icon': detail.get('icon', ''),
            'desc': detail.get('desc', ''),
            'owner': detail.get('owner', ''),
            'createDate': detail.get('createDate', ''),
            'type': detail.get('type', ''),
            'runMethod': detail.get('runMethod', ''),
            'manual': detail.get('manual', False),
            'redirect': detail.get('redirect', '')
        }

    url = 'http://%s%s' % (config.CENTER_HOST, config.LLTS_LIST_URL)
    try:
        rep = requests.get(url)
        tools = json.loads(rep.content)
        return [__getToolInfo(tool) for tool in tools]
    except:
        return []


def start(op, ver, filename, tags):
    if op:
        rep = __callLLTSApi({
            RequestField.TYPE: RequestType.TASK_SUBMIT,
            RequestField.OPERATION: op,
            RequestField.OPERATION_VERSION: ver if ver else '',
	        # RequestField.AGENT_TAG: '',
            RequestField.AGENT_TAG: tags if tags else '',
            # RequestField.VISITOR: config.MCOS_VISITOR,
            # RequestField.VISITOR_TOKEN: config.MCOS_TOKEN,
            'inputFile': filename,
            'role': 'main'
        })
        if rep:
            repObj = json.loads(rep)
            if repObj.get(RequestField.CODE) == 0:
                return repObj.get(RequestField.TASK_ID)
    return None



def kill(id):
    rep = __callLLTSApi({
        RequestField.TYPE: RequestType.TASK_KILL,
        RequestField.TASK_ID: id
    })
    repObj = json.loads(rep)
    return repObj.get(RequestField.CODE) == 0

def getState(id):
    rep = __callLLTSApi({
        RequestField.TYPE: RequestType.TASK_QUERY,
        RequestField.TASK_ID: id
    })
    return json.loads(rep) if rep else {}

def queryClan(id):
    rep = __callLLTSApi({
        RequestField.TYPE: RequestType.TASK_QUERY_CLAN,
        RequestField.TASK_ID: id
    })
    return json.loads(rep) if rep else {}

def queryAgentStat():
    rep = __callLLTSApi({
        RequestField.TYPE: RequestType.AGENT_STATISTIC
    })
    return json.loads(rep) if rep else {}

def getAgentStatistic():
    try:
        rep = requests.get('http://%s%s' % (config.LLTS_TEMPORARY_HOST, config.LLTS_AGENT_STATISTIC))
        return json.loads(rep.content) if rep.content else {}
    except:
        return {}

def getAgentDetail():
    try:
        result = {}
        i = 0
        rep = requests.get('http://%s%s' % (config.LLTS_TEMPORARY_HOST, config.LLTS_AGENT_DETAIL))
        detail = json.loads(rep.content)['data']
        for agentDetail in detail:
            if agentDetail['__AGENT_TAG__'] != json.loads('{}'):
                tags = agentDetail['__AGENT_TAG__']
                for tag in tags.keys():
                    if tag in result:
                        result[tag][agentDetail['__STATUS__']]+=1
                    else:
                        result[tag] = {}
                        result[tag][agentDetail['__STATUS__']] = 1
                        list = ['FREE', 'BUSY', 'LOST']
                        list.remove(agentDetail['__STATUS__'])
                        for i in list:
                            result[tag][i] = 0
        return result
    except:
        return {}
    


