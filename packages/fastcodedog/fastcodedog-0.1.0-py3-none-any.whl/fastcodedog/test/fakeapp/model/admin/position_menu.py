"""
@author: fastcodedog
@project: fakeapp
@file: position_menu.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
岗位和菜单关联
"""
from sqlalchemy import Column, ForeignKey, Integer, Table
from fastcodedog.test.fakeapp.model.base import Base

position_menu = Table('admin_position_menu', Base.metadata,
                      Column('position_id', Integer,
                             ForeignKey('admin_position.id', ondelete='CASCADE'), primary_key=True),
                      Column('menu_id', Integer,
                             ForeignKey('admin_menu.id', ondelete='CASCADE'), primary_key=True)
                      )
