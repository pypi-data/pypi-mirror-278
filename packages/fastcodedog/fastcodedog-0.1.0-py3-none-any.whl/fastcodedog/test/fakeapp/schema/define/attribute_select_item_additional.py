"""
@author: fastcodedog
@project: fakeapp
@file: attribute_select_item_additional.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
schema_additional
"""
from fastcodedog.test.fakeapp.schema.define.attribute_select_item import AttributeSelectItem
from fastcodedog.test.fakeapp.schema.define.attribute import Attribute


class SelectItemWithAttribute(AttributeSelectItem):
    attribute: Attribute = None
