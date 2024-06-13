"""
@author: fastcodedog
@project: fakeapp
@file: attribute_select_item.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性可选项
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class AttributeSelectItemBase(BaseModel):
    parent_id: Optional[int] = Field(None, description="父节点")
    text: Optional[constr(max_length=255)] = Field(None, description="显示文字")
    value: Optional[constr(max_length=255)] = Field(None, description="属性值")
    sort: Optional[int] = Field(None, description="排序")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class AttributeSelectItem(AttributeSelectItemBase):
    id: int = Field(None, description="标识")
    attribute_id: int = Field(None, description="属性定义")


class AttributeSelectItemCreate(AttributeSelectItemBase):
    attribute_id: int = Field(None, description="属性定义")


class AttributeSelectItemUpdate(AttributeSelectItemBase):
    attribute_id: Optional[int] = Field(None, description="属性定义")
