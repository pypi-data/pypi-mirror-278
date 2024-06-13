"""
@author: fastcodedog
@project: fakeapp
@file: organization.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
组织
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class OrganizationBase(BaseModel):
    name: Optional[constr(max_length=255)] = Field(None, description="名称")
    parent_id: Optional[int] = Field(None, description="父节点")
    type: Optional[constr(max_length=64)] = Field(None, description="类型")
    sort: Optional[int] = Field(None, description="排序")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class Organization(OrganizationBase):
    id: int = Field(None, description="标识")
    number: constr(max_length=255) = Field(None, description="编号")


class OrganizationCreate(OrganizationBase):
    number: constr(max_length=255) = Field(None, description="编号")


class OrganizationUpdate(OrganizationBase):
    number: Optional[constr(max_length=255)] = Field(None, description="编号")
