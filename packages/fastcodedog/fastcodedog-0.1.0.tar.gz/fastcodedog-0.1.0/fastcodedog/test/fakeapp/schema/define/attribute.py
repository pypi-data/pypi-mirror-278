"""
@author: fastcodedog
@project: fakeapp
@file: attribute.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性定义
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class AttributeBase(BaseModel):
    object: Optional[constr(max_length=64)] = Field(None, description="目标")
    value_type: Optional[constr(max_length=255)] = Field(None, description="属性值类型")
    enabled: Optional[bool] = Field(None, description="是否启用")
    name: Optional[constr(max_length=255)] = Field(None, description="名称")
    default_value: Optional[constr(max_length=255)] = Field(None, description="默认值")
    remark: Optional[constr(max_length=4096)] = Field(None, description="备注")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class Attribute(AttributeBase):
    id: int = Field(None, description="标识")
    code: constr(max_length=64) = Field(None, description="编码")


class AttributeCreate(AttributeBase):
    code: constr(max_length=64) = Field(None, description="编码")


class AttributeUpdate(AttributeBase):
    code: Optional[constr(max_length=64)] = Field(None, description="编码")
