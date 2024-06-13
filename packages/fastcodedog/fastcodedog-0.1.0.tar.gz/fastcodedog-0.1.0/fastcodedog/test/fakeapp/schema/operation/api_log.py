"""
@author: fastcodedog
@project: fakeapp
@file: api_log.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
接口调用日志表
"""
from pydantic import BaseModel, Field, constr
from typing import Optional
from fastcodedog.util.case_converter import snake_to_camel


class ApiLogBase(BaseModel):
    program: Optional[constr(max_length=64)] = Field(None, description="程序")
    client_ip: Optional[constr(max_length=255)] = Field(None, description="客户IP地址")
    update_date: Optional[str] = Field(None, description="操作时间")
    response_status: Optional[constr(max_length=64)] = Field(None, description="响应状态")
    request_method: Optional[constr(max_length=64)] = Field(None, description="请求方法")
    request_path: Optional[constr(max_length=4096)] = Field(None, description="请求路径")
    request_url: Optional[constr(max_length=4096)] = Field(None, description="请求地址")
    request_head: Optional[str] = Field(None, description="请求头")
    request_body: Optional[str] = Field(None, description="请求体")
    response_time: Optional[int] = Field(None, description="响应时间")
    response_head: Optional[str] = Field(None, description="响应头")
    response_body: Optional[str] = Field(None, description="响应体")
    exception: Optional[str] = Field(None, description="异常")

    class Config:
        extra = 'allow'
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = snake_to_camel


class ApiLog(ApiLogBase):
    id: int = Field(None, description="标识")


class ApiLogCreate(ApiLogBase):
    pass


class ApiLogUpdate(ApiLogBase):
    pass
