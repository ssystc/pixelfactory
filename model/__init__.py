# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import DB_ADDRESS
import config
import traceback


engine = create_engine(DB_ADDRESS, echo = False)
Base = declarative_base()
Session = sessionmaker(bind = engine, expire_on_commit=False)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        config.Log.info(traceback.format_exc())
    finally:
        session.close()


# 导入数据模型
import module
import task
import taskstate
import uidata
import workflow
import logininfo
import redirect
import stateclan
Base.metadata.create_all(engine)
