"""
@author: fastcodedog
@project: fakeapp
@file: tenant.py
@time: 2024-06-12 17:35:41
@desc: 本文件由自动生成脚本自动创建，请勿修改
租户
"""
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from fastcodedog.test.fakeapp.model.base import Base


class Tenant(Base):
    __tablename__ = 'admin_tenant'
    id = Column(Integer, primary_key=True)
    domain = Column(String(64), nullable=False)
    name = Column(String(255), nullable=False)
    enabled = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint(domain),)
