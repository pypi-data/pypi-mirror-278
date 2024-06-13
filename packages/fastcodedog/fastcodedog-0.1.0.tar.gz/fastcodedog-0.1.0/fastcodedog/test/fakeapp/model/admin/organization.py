"""
@author: fastcodedog
@project: fakeapp
@file: organization.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
组织
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class Organization(Base):
    __tablename__ = 'admin_organization'
    id = Column(Integer, primary_key=True, comment='标识')
    number = Column(String(255), nullable=False, comment='编号')
    name = Column(String(255), comment='名称')
    parent_id = Column(Integer, ForeignKey('admin_organization.id'), comment='父节点')
    type = Column(String(64), comment='类型')
    sort = Column(Integer, comment='排序')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    __table_args__ = (UniqueConstraint(number, tenant_id),)
    parent = relationship('Organization', foreign_keys=parent_id, remote_side=id, back_populates='children')
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
    children = relationship('Organization', foreign_keys=parent_id, remote_side=parent_id,
                            cascade='save-update, merge, delete', back_populates='parent')
    users = relationship('User', secondary='admin_user_organization', back_populates='organizations')
