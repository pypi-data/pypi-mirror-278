"""
@author: fastcodedog
@project: fakeapp
@file: attribute_verification.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
属性校验脚本
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class AttributeVerificationBase(BaseModel):
    attribute_id: Optional[int] = Field(None, description="属性定义")
    type: Optional[constr(max_length=64)] = Field(None, description="类型")
    content: Optional[str] = Field(None, description="内容")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class AttributeVerification(AttributeVerificationBase):
    id: int = Field(None, description="标识")


class AttributeVerificationCreate(AttributeVerificationBase):
    pass


class AttributeVerificationUpdate(AttributeVerificationBase):
    pass
