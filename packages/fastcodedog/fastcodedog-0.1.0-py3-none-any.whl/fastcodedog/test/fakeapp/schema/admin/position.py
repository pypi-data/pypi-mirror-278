"""
@author: fastcodedog
@project: fakeapp
@file: position.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
岗位
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class PositionBase(BaseModel):
    name: Optional[constr(max_length=255)] = Field(None, description="名称")
    remark: Optional[constr(max_length=4096)] = Field(None, description="备注")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class Position(PositionBase):
    id: int = Field(None, description="标识")
    number: constr(max_length=64) = Field(None, description="编号")


class PositionCreate(PositionBase):
    number: constr(max_length=64) = Field(None, description="编号")


class PositionUpdate(PositionBase):
    number: Optional[constr(max_length=64)] = Field(None, description="编号")
