# coding: utf-8

from . import Base, session_scope
from sqlalchemy import String, UnicodeText, Column
from common.const import ErrorCode
import uuid

class ModuleState(Base):
    __tablename__ = 'modulestate'

    id = Column(String, default=lambda: uuid.uuid4().hex, primary_key=True)
    content = Column(UnicodeText)
    userId = Column(String)

    def __init__(self, content):
        self.content = content

    
class ModuleStateDao(object):

    @classmethod
    def add(cls, ms):
        with session_scope() as session:
            session.add(ms)
        return ms.id

    @classmethod
    def query(cls, id):
        with session_scope() as session:
            try:
                return session.query(ModuleState).filter(ModuleState.id==id).one()
            except:
                return None