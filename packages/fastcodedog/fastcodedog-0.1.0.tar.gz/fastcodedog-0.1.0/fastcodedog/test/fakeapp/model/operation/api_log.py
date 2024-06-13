"""
@author: fastcodedog
@project: fakeapp
@file: api_log.py
@time: 2024-06-12 15:34:18
@desc: 本文件由自动生成脚本自动创建，请勿修改
接口调用日志表
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from fastcodedog.test.fakeapp.model.base import Base


class ApiLog(Base):
    __tablename__ = 'operation_api_log'
    id = Column(Integer, primary_key=True, comment='标识')
    program = Column(String(64), comment='程序')
    client_ip = Column(String(255), comment='客户IP地址')
    update_date = Column(DateTime, comment='操作时间')
    response_status = Column(String(64), comment='响应状态')
    request_method = Column(String(64), comment='请求方法')
    request_path = Column(String(4096), comment='请求路径')
    request_url = Column(String(4096), comment='请求地址')
    request_head = Column(Text, comment='请求头')
    request_body = Column(Text, comment='请求体')
    response_time = Column(Integer, comment='响应时间')
    response_head = Column(Text, comment='响应头')
    response_body = Column(Text, comment='响应体')
    exception = Column(Text, comment='异常')
