"""
@author: fastcodedog
@project: fakeapp
@file: user.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
用户
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class User(Base):
    __tablename__ = 'admin_user'
    id = Column(Integer, primary_key=True, comment='标识')
    number = Column(String(255), nullable=False, comment='工号')
    password = Column(String(255), comment='密码')
    name = Column(String(255), comment='名称')
    telephone = Column(String(255), comment='电话')
    email = Column(String(255), comment='邮箱')
    head_url = Column(String(4096), comment='头像')
    state_valid = Column(String(64), comment='有效状态')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    __table_args__ = (UniqueConstraint(number, tenant_id),)
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
    organizations = relationship('Organization', secondary='admin_user_organization', back_populates='users')
    positions = relationship('Position', secondary='admin_user_position', back_populates='users')
