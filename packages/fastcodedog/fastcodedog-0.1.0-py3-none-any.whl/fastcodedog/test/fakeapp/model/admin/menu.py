"""
@author: fastcodedog
@project: fakeapp
@file: menu.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
菜单
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class Menu(Base):
    __tablename__ = 'admin_menu'
    id = Column(Integer, primary_key=True, comment='标识')
    number = Column(String(64), nullable=False, comment='编号')
    platform = Column(String(64), comment='平台')
    sort = Column(Integer, comment='排序')
    type = Column(String(64), comment='类型')
    parent_id = Column(Integer, ForeignKey('admin_menu.id'), comment='父节点')
    name = Column(String(255), comment='名称')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    __table_args__ = (UniqueConstraint(number, tenant_id),)
    parent = relationship('Menu', foreign_keys=parent_id, remote_side=id, back_populates='children')
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
    positions = relationship('Position', secondary='admin_position_menu', back_populates='menus')
    children = relationship('Menu', foreign_keys=parent_id, remote_side=parent_id,
                            cascade='save-update, merge, delete', back_populates='parent')
