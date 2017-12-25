# coding: utf-8

from common.const import ErrorCode, TaskMessageField, TaskRequestType
from workflow import Workflow
from model.logininfo import LoginInfoDao
import config
import os
import shutil
from model.stateclan import StateClan, StateClanDao


class TaskMgr(object):

    tasks = {}

    @classmethod
    def __getUserId(cls, uid):
        return LoginInfoDao.getUserId(uid)

    @classmethod
    def __doOption(cls, msg, func):
        taskId = msg[TaskMessageField.Id]
        taskType = msg[TaskMessageField.Type]
        code = ErrorCode.NoError
        if taskId in cls.tasks:
            code = getattr(cls.tasks[taskId], func)()
        else:
            code = ErrorCode.TaskNotInRuning
        return {
            TaskMessageField.Id: taskId,
            TaskMessageField.Type: taskType,
            TaskMessageField.ErrCode: code
        }

    @classmethod
    def startTask(cls, msg):
        taskId = msg[TaskMessageField.Id]
        taskType = msg[TaskMessageField.Type]
        StateClanDao.deleteByTaskId(taskId, cls.__getUserId(msg[TaskMessageField.UserUid]))
        taskdir = '%s%s' % (config.FILE_SYSTEM_ROOT, taskId)
        # if os.path.exists(taskdir):
	    # shutil.rmtree(taskdir)
	
	
        # 防止重复提交任务
        if taskId in cls.tasks and not cls.tasks[taskId].isOver():
            config.Log.info(u'task %s is already runing.' % taskId)
            return {
                TaskMessageField.Id: taskId,
                TaskMessageField.Type: taskType,
                TaskMessageField.ErrCode: ErrorCode.TaskAlreadyInRuning
            }

        userId = cls.__getUserId(msg[TaskMessageField.UserUid])

        if not userId:
            config.Log.info(u"task can't start because user is None.")
            return {
                TaskMessageField.Id: taskId,
                TaskMessageField.Type: taskType,
                TaskMessageField.ErrCode: ErrorCode.TaskStartNoUser
            }

        content = msg[TaskMessageField.Content]
        flow = content['flow']
        task = content['task']
        workflow = Workflow(task, flow, userId)
        cls.tasks[taskId] = workflow
        return cls.__doOption(msg, 'startRun')

    @classmethod
    def pauseTask(cls, msg):
        return cls.__doOption(msg, 'pauseRun')

    @classmethod
    def continueTask(cls, msg):
        return cls.__doOption(msg, 'continueRun')

    @classmethod
    def stopTask(cls, msg):
        return cls.__doOption(msg, 'stopRun')

    @classmethod
    def queryTaskState(cls, msg):
        taskId = msg[TaskMessageField.Id]
        taskType = msg[TaskMessageField.Type]
        state = {}
        code = ErrorCode.NoError
        if taskId in cls.tasks:
            state = cls.tasks[taskId].getState()
        else:
            code = ErrorCode.TaskNotFind
        return {
            TaskMessageField.Id: taskId,
            TaskMessageField.Type: taskType,
            TaskMessageField.ErrCode: code,
            TaskMessageField.Content: state
        }

