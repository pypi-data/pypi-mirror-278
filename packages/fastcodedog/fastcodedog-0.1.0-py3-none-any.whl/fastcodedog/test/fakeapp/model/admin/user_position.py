"""
@author: fastcodedog
@project: fakeapp
@file: user_position.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
用户岗位
"""
from sqlalchemy import Column, ForeignKey, Integer, Table
from fastcodedog.test.fakeapp.model.base import Base

user_position = Table('admin_user_position', Base.metadata,
                      Column('user_id', Integer,
                             ForeignKey('admin_user.id', ondelete='CASCADE'), primary_key=True),
                      Column('position_id', Integer,
                             ForeignKey('admin_position.id', ondelete='CASCADE'), primary_key=True)
                      )
