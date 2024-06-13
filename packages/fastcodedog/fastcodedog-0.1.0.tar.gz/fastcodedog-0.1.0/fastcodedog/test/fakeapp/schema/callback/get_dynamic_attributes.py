"""
@author: fastcodedog
@project: fakeapp
@file: get_dynamic_attributes.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
获取动态属性的例子
"""
from pydantic import Field
from typing import Optional


def get_dynamic_attributes(table_name: str = None):
    # extra_attribute_sample: Optional[str]= Field(None, exclude_none=True, description='a sample of extra attribute')
    return {{'extra_attribute_sample': (Optional[str], Field(None, exclude_none=True, description='a sample of extra attribute'))}}
