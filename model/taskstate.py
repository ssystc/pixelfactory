# coding: utf-8

from . import Base, session_scope
from sqlalchemy import Integer, Float, String, UnicodeText, Column, ForeignKey, desc
from sqlalchemy.orm import relationship
from common.const import ErrorCode
import uuid
import json
import traceback
import config

# 任务名称、所属流程、开始时间、结束时间、状态、当前步骤、失败原因


class TaskState(Base):
    
    __tablename__ = 'taskstate'

    id = Column(String, default=lambda: uuid.uuid4().hex, primary_key=True)
    taskId = Column(String, ForeignKey('task.id'))
    paused = Column(Integer)
    submitTime = Column(Float)
    startTime = Column(Float)
    endTime = Column(Float)
    clan = Column(UnicodeText)
    fsId = Column(String)
    taskname = Column(UnicodeText)
    flowId = Column(String)
    flowname = Column(UnicodeText)
    status = Column(UnicodeText)
    errinfo = Column(UnicodeText)
    userId = Column(String)
    
    

    task = relationship('Task', back_populates='taskstates')

    def __init__(self, taskId, paused, submitTime, startTime, endTime, clan, fsId, taskname, flowId, flowname, status, errinfo,userId = None):
        self.taskId = taskId
        self.paused = int(paused)
        self.submitTime = submitTime
        self.startTime = startTime
        self.endTime = endTime
        self.clan = unicode(json.dumps(clan, ensure_ascii=False)) if isinstance(clan, dict) else clan
        self.fsId = fsId
        self.taskname = taskname
        self.flowId = flowId
        self.flowname = flowname
        self.status = status
        self.errinfo = errinfo
        self.userId = userId
        

    def dumpDetail(self):
        return {
            'id': self.id,
            'taskId': self.taskId,
            'paused': self.paused,
            'submitTime': self.submitTime,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'clan': self.clan,
            'fsId': self.fsId,
            'taskname': self.taskname,
            'flowId': self.flowId,
            'flowname': self.flowname,
            'status': self.status,
            'errinfo': self.errinfo,
            'userId': self.userId
        }


class TaskStateDao(object):

    @classmethod
    def addTaskState(cls, taskstate):
        with session_scope() as session:
            session.add(taskstate)
        return taskstate.id

    @classmethod
    def modifyTaskState(cls, id, taskstate, userId):
        with session_scope() as session:
            ts = session.query(TaskState).filter(TaskState.id == id, taskstate.userId == userId).one()
            ts.taskId = taskstate.taskId
            ts.paused = taskstate.paused
            ts.submitTime = taskstate.submitTime
            ts.startTime = taskstate.startTime
            ts.endTime = taskstate.endTime
            ts.clan = taskstate.clan
            ts.fsId = taskstate.fsId
            ts.taskname = taskstate.taskname
            ts.flowId = taskstate.flowId
            ts.flowname = taskstate.flowname
            ts.status = taskstate.status
            ts.errinfo = taskstate.errinfo
            ts.userId = taskstate.userId


    @classmethod
    def queryByFsId(cls, fsId, userId):
        with session_scope() as session:
            try:
                return session.query(TaskState.id).filter(TaskState.fsId == str(fsId)).order_by(desc(TaskState.submitTime)).first()
            except:
                config.Log.info(traceback.format_exc())
                return None

    # 获取最近一次的任务状态
    @classmethod
    def lastTaskState(cls, taskId, userId):
        with session_scope() as session:
            try:
                return session.query(TaskState).filter(TaskState.taskId == taskId, TaskState.userId == userId).order_by(desc(TaskState.submitTime)).first()
            except:
                return None



    @classmethod
    def deleteTaskState(cls, id, userId):
        with session_scope() as session:
            try:
                taskstate = session.query(TaskState).filter(TaskState.taskId == id, TaskState.userId == userId).delete()
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindTaskStateById



    @classmethod
    # 参数分别是排序列名，排序方式（升序降序），一页有多少数据，从第几页开始，预留的searchText字段
    def queryByArgs(cls, sortName, sortOrder, pageSize, pageNumber, userId, searchText=None):
        with session_scope() as session:
            try:
                pageSize = int(pageSize)
                pageNumber = int(pageNumber)
                str = 'StateClan.%s' % sortName
                if sortOrder == 'asc':
                    statelist = session.query(TaskState).filter(TaskState.userId == userId).order_by(eval(str)).limit(pageSize).offset(pageSize * (pageNumber - 1)).all()
                    return statelist
                elif sortOrder == 'desc':
                    statelist = session.query(TaskState).filter(TaskState.userId == userId).order_by(desc(eval(str))).limit(pageSize).offset(pageSize * (pageNumber - 1)).all()
                    return statelist
                else:
                    return None
            except:
                return None
            
        
    @classmethod
    def queryCount(cls, userId):
        with session_scope() as session:
            try:
                count = session.query(TaskState).filter(TaskState.userId == userId).count()
                return count
            except:
                return None
            
