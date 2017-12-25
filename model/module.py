# coding: utf-8

from . import Base, session_scope
from sqlalchemy import String, Column, UnicodeText
import uuid
import json

class Module(Base):
    __tablename__ = 'module'

    id = Column(String, default=lambda: uuid.uuid4().hex, primary_key=True)
    content = Column(UnicodeText)

    def dumpInfo(self):
        detail = json.loads(self.content)
        return {
            'id': self.id,
            'name': detail.get('name', ''),
            'icon': detail.get('icon', ''),
            'desc': detail.get('desc', ''),
            'owner': detail.get('owner', ''),
            'createDate': detail.get('createDate', ''),
            'type': detail.get('type', ''),
            'runMethod': detail.get('runMethod', ''),
            'manual': detail.get('manual', False),
            'redirect': detail.get('redirect', ''),
            'ModuleClass': detail.get('ModuleClass', '')
        }

    def dumpDetail(self):
        detail = json.loads(self.content)
        detail['id'] = self.id
        return detail


class ModuleDao(object):

    @classmethod
    def modulesList(cls):
        with session_scope() as session:
            modules = session.query(Module).all() or []
        return [module.dumpInfo() for module in modules]

    @classmethod
    def queryModule(cls, id):
        with session_scope() as session:
            try:
                module = session.query(Module).filter_by(id=id).one()
                return module.dumpDetail()
            except:
                return {}
