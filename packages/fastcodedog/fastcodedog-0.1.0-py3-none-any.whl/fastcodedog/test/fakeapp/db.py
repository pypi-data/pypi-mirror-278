"""
@author: fastcodedog
@project: fakeapp
@file: db.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config.config import db_url

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
