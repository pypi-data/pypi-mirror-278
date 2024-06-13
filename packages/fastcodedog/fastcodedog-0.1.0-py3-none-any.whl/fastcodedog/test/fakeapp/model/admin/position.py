"""
@author: fastcodedog
@project: fakeapp
@file: position.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
岗位
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class Position(Base):
    __tablename__ = 'admin_position'
    id = Column(Integer, primary_key=True, comment='标识')
    number = Column(String(64), nullable=False, comment='编号')
    name = Column(String(255), comment='名称')
    remark = Column(String(4096), comment='备注')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    __table_args__ = (UniqueConstraint(number, tenant_id),)
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
    menus = relationship('Menu', secondary='admin_position_menu', back_populates='positions')
    users = relationship('User', secondary='admin_user_position', back_populates='positions')
