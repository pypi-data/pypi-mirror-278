"""
@author: fastcodedog
@project: fakeapp
@file: attribute_verification.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性校验脚本
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from fastcodedog.test.fakeapp.model.base import Base


class AttributeVerification(Base):
    __tablename__ = 'define_attribute_verification'
    id = Column(Integer, primary_key=True, comment='标识')
    attribute_id = Column(Integer, ForeignKey('define_attribute.id'), comment='属性定义')
    type = Column(String(64), comment='类型')
    content = Column(Text, comment='内容')
    tenant_id = Column(Integer, ForeignKey('admin_tenant.id'), nullable=False, comment='租户')

    attribute = relationship('Attribute', foreign_keys=attribute_id, back_populates='attribute_verifications')
    tenant = relationship('Tenant', foreign_keys=tenant_id)  # no_back_populates
