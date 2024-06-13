"""
@author: fastcodedog
@project: fakeapp
@file: user.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
用户
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class UserBase(BaseModel):
    name: Optional[constr(max_length=255)] = Field(None, description="名称")
    telephone: Optional[constr(max_length=255)] = Field(None, description="电话")
    email: Optional[constr(max_length=255)] = Field(None, description="邮箱")
    head_url: Optional[constr(max_length=4096)] = Field(None, description="头像")
    state_valid: Optional[constr(max_length=64)] = Field(None, description="有效状态")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class User(UserBase):
    id: int = Field(None, description="标识")
    number: constr(max_length=255) = Field(None, description="工号")


class UserCreate(UserBase):
    number: constr(max_length=255) = Field(None, description="工号")
    password: Optional[constr(max_length=255)] = Field(None, description="密码")


class UserUpdate(UserBase):
    number: Optional[constr(max_length=255)] = Field(None, description="工号")
    password: Optional[constr(max_length=255)] = Field(None, description="密码")
