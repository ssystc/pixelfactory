# coding: utf-8

from . import Base, session_scope
from sqlalchemy import Integer, String, UnicodeText, Column, ForeignKey
from sqlalchemy.orm import relationship
from common.const import ErrorCode
import traceback
import config
import uuid


class UiData(Base):
    __tablename__ = 'uidata'

    id = Column(String, primary_key=True)
    flowId = Column(String, ForeignKey('workflow.id'), unique = True)
    content = Column(UnicodeText)
    userId = Column(String)

    workflow = relationship('WorkFlow', back_populates='uidata')

    def __init__(self, flowId, content, userId, uidataid = uuid.uuid4()):
        self.flowId = flowId
        self.content = content
        self.userId = userId
        self.id = uidataid	

class UiDataDao(object):

    @classmethod
    def _getData(cls, flowId, userId):
        with session_scope() as session:
            try:
                return session.query(UiData).filter(UiData.flowId == flowId, UiData.userId == userId).one()
            except:
                return None

    @classmethod
    def getData(cls, flowId, userId):
        uidata = cls._getData(flowId, userId)
        return uidata.content if uidata else ''

    @classmethod
    def setData(cls, flowId, content, userId):
        with session_scope() as session:
            try:
                uidata = session.query(UiData).filter(UiData.flowId==flowId, UiData.userId == userId).one()
                uidata.content = content
            except:
                try:
                    uidata = UiData(flowId, content, userId, uuid.uuid4())
                    session.add(uidata)
                except:
                    config.Log.info(traceback.format_exc())
        return ErrorCode.NoError



    @classmethod
    def deleteUiDataByFlowId(cls, flowId, userId):
        with session_scope() as session:
            try:
                uidata = session.query(UiData).filter(UiData.flowId == flowId, UiData.userId == userId).delete()
                return ErrorCode.NoError
            except:
                return ErrorCode.NotFindUiDataByFlowId
