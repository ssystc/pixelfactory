# coding: utf-8


from sqlalchemy import String, Column
from model import Base, session_scope

class Redirect(Base):

    __tablename__ = 'redirect'
    uid = Column(String, primary_key=True)
    url = Column(String)

    def __init__(self, uid, url):
        self.uid = uid
        self.url = url


class RedirectDao(object):

    @classmethod
    def queryUrl(cls, uid):
        try:
            with session_scope() as session:
                redirect = session.query(Redirect).filter(Redirect.uid == uid).one()
                return redirect.url
        except:
            return None

    @classmethod
    def add(cls, redirect):
        with session_scope() as session:
            session.add(redirect)

    @classmethod
    def delete(cls, uid):
        with session_scope() as session:
            session.query(Redirect).filter(Redirect.uid == uid).delete()

    @classmethod
    def pop(cls, uid):
        with session_scope() as session:
            try:
                redirect = session.query(Redirect).filter(Redirect.uid == uid).one()
                session.delete(redirect)
                url = redirect.url
                return url
            except:
                return None

    @classmethod
    def deleteAll(cls):
        with session_scope() as session:
            session.query(Redirect).filter().delete()