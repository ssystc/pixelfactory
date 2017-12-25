# coding: utf-8

import traceback
from . import Base, session_scope
from sqlalchemy import String, UnicodeText, Column, ForeignKey
from sqlalchemy.orm import relationship
from common.const import ErrorCode
from taskstate import TaskState
import uuid
import json
import config

class Task(Base):
    __tablename__ = 'task'

    id = Column(String, default=lambda: uuid.uuid4().hex, primary_key=True)
    content = Column(UnicodeText)
    name = Column(UnicodeText)
    desc = Column(UnicodeText)
    owner = Column(UnicodeText)
    createDate = Column(UnicodeText)
    dir = Column(UnicodeText)
    dirclassify = Column(UnicodeText)
    icon = Column(String)
    flowId = Column(String, ForeignKey('workflow.id'))
    userId = Column(String)

    workflow = relationship('WorkFlow', back_populates='tasks')
    taskstates = relationship('TaskState', back_populates='task', order_by=TaskState.id, cascade='all, delete, delete-orphan')
    # stateclans = relationship('StateClan', back_populates='task', cascade='all, delete, delete-orphan')

    def __init__(self, content, userId):
        self.setupByContent(content)
        self.userId = userId

    def setupByContent(self, content):
        contentObj = json.loads(content)
        self.name = contentObj.get('name', '')
        self.desc = contentObj.get('desc', '')
        self.owner = contentObj.get('owner', '')
        self.createDate = contentObj.get('createDate', '')
        self.dir = contentObj.get('dir', '')
        self.flowId = contentObj.get('flowId', '')
        self.icon = contentObj.get('icon', '')
        self.dirclassify = contentObj.get('dirclassify', '')
        self.content = content

    def dumpInfo(self):
        return {
            'id': self.id,
            'flowId': self.flowId,
            'name': self.name,
            'desc': self.desc,
            'owner': self.owner,
            'createDate': self.createDate,
            'dir': self.dir,
            'icon': self.icon,
            'dirclassify': self.dirclassify
        }

    def dumpDetail(self):
        contentObj = json.loads(self.content)
        contentObj['id'] = self.id
        return contentObj


class TaskDao():

    @classmethod
    def saveTask(cls, task):
        with session_scope() as session:
            flowId = task.flowId
            userid = task.userId
            tastNameList = TaskDao.queryTaskNameByFlowId(flowId, userid)
            if task.name in tastNameList:
                return ErrorCode.AddDuplicationTaskName
            session.add(task)
            return ErrorCode.NoError

    @classmethod
    def updateTask(cls, id, content, userId):
        with session_scope() as session:
            try:
                task = session.query(Task).filter(Task.id == id, Task.userId == userId).one()
                task.setupByContent(content)
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindTaskById

    @classmethod
    def deleteTask(cls, id, userId):
        with session_scope() as session:
            try:
                task = session.query(Task).filter(Task.id == id, Task.userId == userId).delete()
                return ErrorCode.NoError
            except:
                return traceback.format_exc()

    @classmethod
    def queryTask(cls, id, userId):
        with session_scope() as session:
            try:
                return session.query(Task).filter(Task.id == id, Task.userId == userId).one()
            except:
                return None

    @classmethod
    def taskList(cls, userId, flowId = None):
        with session_scope() as session:
            try:
                if flowId:
                    return session.query(Task).filter(Task.flowId == flowId, Task.userId == userId).all()
                else:
                    return session.query(Task).filter(Task.userId == userId).all()
            except:
                return []

    @classmethod
    def taskCount(cls, flowId = None):
        with session_scope() as session:
            if flowId:
                return session.query(Task).filter(Task.flowId==flowId).count()
            else:
                return session.query(Task).count()


    @classmethod
    def deleteByFlowId(cls, flowId, userId):
        with session_scope() as session:
            try:
                task = session.query(Task).filter(Task.flowId == flowId, Task.userId == userId).delete()
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindTaskById


    @classmethod
    def queryTaskIdByFlowId(cls, flowId, userId):
        taskIdList = []
        with session_scope() as session:
            try:
                list = session.query(Task).filter(Task.flowId == flowId, Task.userId == userId).all()
                for info in list:
                    taskIdList.append(info.id)
                return taskIdList
            except:
                return []
            
    @classmethod
    def queryTaskNameByFlowId(cls, flowId, userId):
        taskNameList = []
        with session_scope() as session:
            try:
                list = session.query(Task).filter(Task.flowId == flowId, Task.userId == userId).all()
                for info in list:
                    taskNameList.append(info.name)
                return taskNameList
            except:
                return []

