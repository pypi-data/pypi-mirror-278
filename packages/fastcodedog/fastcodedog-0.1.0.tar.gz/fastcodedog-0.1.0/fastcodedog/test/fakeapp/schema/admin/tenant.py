"""
@author: fastcodedog
@project: fakeapp
@file: tenant.py
@time: 2024-06-12 16:56:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
租户
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class TenantBase(BaseModel):
    pass

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class Tenant(TenantBase):
    id: int = Field(None)
    domain: constr(max_length=64) = Field(None)
    name: constr(max_length=255) = Field(None)
    enabled: bool = Field(None)


class TenantCreate(TenantBase):
    domain: constr(max_length=64) = Field(None)
    name: constr(max_length=255) = Field(None)
    enabled: bool = Field(None)


class TenantUpdate(TenantBase):
    domain: Optional[constr(max_length=64)] = Field(None)
    name: Optional[constr(max_length=255)] = Field(None)
    enabled: Optional[bool] = Field(None)
