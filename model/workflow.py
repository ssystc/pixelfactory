# coding: utf-8

from . import Base, session_scope
from sqlalchemy import String, UnicodeText, Column, or_, and_
from sqlalchemy.orm import relationship
import json
import uuid
from common.const import ErrorCode
from task import Task
from uidata import UiData

class WorkFlow(Base):
    __tablename__ = 'workflow'

    # id = db.Column(db.Integer, primary_key=True)

    # 使用uuid作为主键
    id = Column(String, default=lambda: uuid.uuid4().hex, primary_key=True)
    
    name = Column(UnicodeText)
    icon = Column(UnicodeText)
    desc = Column(UnicodeText)
    owner = Column(UnicodeText)
    createDate = Column(UnicodeText)
    type = Column(String)
    runMethod = Column(UnicodeText)
    version = Column(UnicodeText)
    content = Column(UnicodeText)
    key = Column(UnicodeText)
    userId = Column(String)
    subkey = Column(UnicodeText)

    tasks = relationship('Task', back_populates='workflow', order_by=Task.id, cascade='all, delete, delete-orphan')
    uidata = relationship('UiData', back_populates='workflow', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '<%s \n %s \n %s>' % (id, self.name, self.content)

    def __init__(self, content, userId):
        self.setupByContent(content)
        self.userId = userId

    def setupByContent(self, content):
        contentObj = json.loads(content)
        self.name = contentObj.get('name', u'')
        self.icon = contentObj.get('icon', u'')
        self.desc = contentObj.get('desc', u'')
        self.owner = contentObj.get('owner', u'')
        self.createDate = contentObj.get('createDate', u'')
        self.type = contentObj.get('type', u'')
        self.runMethod = contentObj.get('runMethod', u'')
        self.version = contentObj.get('version', u'')
        self.key = contentObj.get('key', u'')
        self.content = content
        self.subkey = contentObj.get('subkey', u'')

    def dumpInfo(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'desc': self.desc,
            'owner': self.owner,
            'createDate': self.createDate,
            'type': self.type,
            'runMethod': self.runMethod,
            'key': self.key,
            'version': self.version,
            'subkey': self.subkey
        }

    def dumpDetail(self):
        contentObj = json.loads(self.content)
        contentObj['name'] = self.name
        contentObj['icon'] = self.icon
        contentObj['desc'] = self.desc
        contentObj['owner'] = self.owner
        contentObj['createDate'] = self.createDate
        contentObj['type'] = self.type
        contentObj['runMethod'] = self.runMethod
        contentObj['version'] = self.version
        contentObj['id'] = self.id
        contentObj['key'] = self.key
        contentObj['subkey'] = self.subkey
        return contentObj

class WorkFlowDao():
    
    @classmethod
    def saveWorkflow(cls, workflow):
        with session_scope() as session:
            session.add(workflow)
        return ErrorCode.NoError

    @classmethod
    def updateWorkflow(cls, id, content, userId):
        with session_scope() as session:
            try:
                wf = session.query(WorkFlow).filter(WorkFlow.id==id, WorkFlow.userId == userId).one()
                wf.setupByContent(content)
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindFlowById

    @classmethod
    def deleteWorkflow(cls, id, userId):
        with session_scope() as session:
            try:
                session.query(WorkFlow).filter(WorkFlow.id == id, WorkFlow.userId == userId).delete()
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindFlowById

    @classmethod
    def queryWorkflow(cls, id, userId):
        with session_scope() as session:
            try:
                return session.query(WorkFlow).filter(or_(and_(WorkFlow.id == id, WorkFlow.userId == userId),(and_(WorkFlow.id == id, WorkFlow.type == 'mutual')))).one()
            except:
                return None

    @classmethod
    def queryByKey(cls, key, userId):
        with session_scope() as session:
            try:
                return session.query(WorkFlow).filter(or_(and_(WorkFlow.key == key, WorkFlow.userId == userId), (and_(WorkFlow.key == key, WorkFlow.type == 'mutual')))).all()
            except:
                return []
    
    @classmethod
    def getMutualFlowList(cls):
        with session_scope() as session:
            try:
                return session.query(WorkFlow).filter(WorkFlow.type == u'mutual').all()
            except:
                return []
    
    @classmethod
    def workflowList(cls, userId):
        with session_scope() as session:
            try:
                return session.query(WorkFlow).filter(or_(WorkFlow.userId == userId, WorkFlow.type == u'mutual')).all()
            except:
                return []
            
