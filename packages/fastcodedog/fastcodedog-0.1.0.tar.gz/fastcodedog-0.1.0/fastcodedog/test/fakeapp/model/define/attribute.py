"""
@author: fastcodedog
@project: fakeapp
@file: attribute.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性定义
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class Attribute(Base):
    __tablename__ = 'define_attribute'
    id = Column(Integer, primary_key=True, comment='标识')
    code = Column(String(64), nullable=False, comment='编码')
    object = Column(String(64), comment='目标')
    value_type = Column(String(255), comment='属性值类型')
    enabled = Column(Boolean, comment='是否启用')
    name = Column(String(255), comment='名称')
    default_value = Column(String(255), comment='默认值')
    remark = Column(String(4096), comment='备注')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    __table_args__ = (UniqueConstraint(code, object, tenant_id),)
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
    attribute_select_items = relationship(
        'AttributeSelectItem', cascade='save-update, merge, delete', back_populates='attribute')
    attribute_verifications = relationship(
        'AttributeVerification', cascade='save-update, merge, delete', back_populates='attribute')
