"""
@author: fastcodedog
@project: fakeapp
@file: attribute_select_item.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.define.attribute_select_item import AttributeSelectItem


def create_attribute_select_item(session, attribute_select_item_create):
    attribute_select_item = AttributeSelectItem(**attribute_select_item_create.dict(exclude_unset=True))
    session.add(attribute_select_item)
    session.commit()
    return attribute_select_item


def update_attribute_select_item(session, attribute_select_item_id: int, attribute_select_item_update):
    attribute_select_item = session.query(AttributeSelectItem).filter(
        AttributeSelectItem.id == attribute_select_item_id).first()
    if attribute_select_item:
        for key, value in attribute_select_item_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(attribute_select_item, key, value)
        session.commit()
    return attribute_select_item


def delete_attribute_select_item(session, attribute_select_item_id: int):
    attribute_select_item = session.query(AttributeSelectItem).filter(
        AttributeSelectItem.id == attribute_select_item_id).first()
    if attribute_select_item:
        session.delete(attribute_select_item)
        session.commit()
    return


def get_attribute_select_item(session, attribute_select_item_id: int):
    attribute_select_item = session.query(AttributeSelectItem).filter(
        AttributeSelectItem.id == attribute_select_item_id).first()
    return attribute_select_item
