"""
@author: fastcodedog
@project: fakeapp
@file: attribute.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.define.attribute import Attribute


def create_attribute(session, attribute_create):
    attribute = Attribute(**attribute_create.dict(exclude_unset=True))
    session.add(attribute)
    session.commit()
    return attribute


def update_attribute(session, attribute_id: int, attribute_update):
    attribute = session.query(Attribute).filter(Attribute.id == attribute_id).first()
    if attribute:
        for key, value in attribute_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(attribute, key, value)
        session.commit()
    return attribute


def delete_attribute(session, attribute_id: int):
    attribute = session.query(Attribute).filter(Attribute.id == attribute_id).first()
    if attribute:
        session.delete(attribute)
        session.commit()
    return


def get_attribute(session, attribute_id: int):
    attribute = session.query(Attribute).filter(Attribute.id == attribute_id).first()
    return attribute
