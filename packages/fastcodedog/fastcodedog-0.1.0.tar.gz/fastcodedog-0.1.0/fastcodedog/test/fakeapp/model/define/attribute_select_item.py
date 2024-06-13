"""
@author: fastcodedog
@project: fakeapp
@file: attribute_select_item.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性可选项
"""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class AttributeSelectItem(Base):
    __tablename__ = 'define_attribute_select_item'
    id = Column(Integer, primary_key=True, comment='标识')
    attribute_id = Column(Integer, ForeignKey('define_attribute.id'), nullable=False, comment='属性定义')
    parent_id = Column(Integer, comment='父节点')
    text = Column(String(255), comment='显示文字')
    value = Column(String(255), comment='属性值')
    sort = Column(Integer, comment='排序')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    attribute = relationship('Attribute', foreign_keys=attribute_id, back_populates='attribute_select_items')
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
