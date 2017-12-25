# coding: utf-8

class RequestType(object):
    TASK_SUBMIT = 'TASK/SUBMIT'  # client => controller
    TASK_KILL = 'TASK/KILL'  # client => controller => agent
    TASK_QUERY = 'TASK/QUERY'  # client => controller
    TASK_QUERY_CLAN = 'TASK/QUERY_CLAN'  # client => controller

    AGENT_HEARTBEAT = 'AGENT/HEARTBEAT'  # agent => controller
    AGENT_EXIT = 'AGENT/EXIT'  # agent => controller
    AGENT_STOP = 'AGENT/STOP'  # controller => agent

    TASK_INFORM = 'TASK/INFORM'  # controller => agent
    TASK_APPLY = 'TASK/INTERNAL/APPLY'  # agent => controller
    TASK_REPORT = 'TASK/INTERNAL/REPORT'  # agent => controller

    TASK_STATISTIC = 'TASK/STATISTIC'  # client => controller
    AGENT_STATISTIC = 'AGENT/STATISTIC'  # client => controller

    TASK_DETAILS = 'TASK/DETAILS'  # client => controller
    AGENT_DETAILS = 'AGENT/DETAILS'  # client => controller
    TOOL_DETAILS = 'TOOL/DETAILS'  # client => controller


class AgentStatus(object):
    LOST = "LOST"
    BUSY = "BUSY"
    FREE = "FREE"


class TaskStatus(object):
    WAITING = 'WAITING'
    DISPATCHED = 'DISPATCHED'
    PREPARING = 'PREPARING'
    RUNNING = 'RUNNING'
    ENDED = 'ENDED'
    FINISHED = 'FINISHED'


class RequestField(object):
    TYPE = '__TYPE__'
    CODE = '__CODE__'
    TIME = '__TIME__'
    EXIT_CODE = '__EXIT_CODE__'
    STATUS = '__STATUS__'
    AGENT_STATUS = '__AGENT_STATUS__'
    OPERATION = '__OPERATION__'
    VISITOR = '__VISITOR__'
    VISITOR_TOKEN = '__VISITOR_TOKEN__'
    OPERATION_VERSION = '__OPERATION_VERSION__'
    TASK_ID = '__TASK_ID__'
    AGENT_TAG = '__AGENT_TAG__'
    AGENT_IP = '__AGENT_IP__'
    PROCESS_ID = '__PROCESS_ID__'
    PROCESS_STATUS = '__PROCESS_STATUS__'
    AGENT_ID = '__AGENT_ID__'
    FATHER_ID = '__FATHER_ID__'
    WORK_DIR = '__WORK_DIR__'
    ADDRESS = '__ADDRESS__'
    REPORT_LOG = '__REPORT_LOG__'

    SUBMIT_TIME = '__SUBMIT_TIME__'
    PREPARE_TIME = '__PREPARE_TIME__'
    RUN_TIME = '__RUN_TIME__'
    KILLED = '__KILLED__'
    KILL_TIME = '__KILL_TIME__'
    END_TIME = '__END_TIME__'
    FINISH_TIME = '__FINISH_TIME__'

    TOOL_NAME = '__TOOL_NAME__'
    TOOL_VERSION = '__TOOL_VERSION__'
    TOOL_PATH = '__TOOL_PATH__'

    CLAN_STATISTIC = '__CLAN_STATISTIC__'
    CLAN_TASKS = '__CLAN__'
