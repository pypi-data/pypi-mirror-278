"""
@author: fastcodedog
@project: fakeapp
@file: api_log.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.operation.api_log import ApiLog


def create_api_log(session, api_log_create):
    api_log = ApiLog(**api_log_create.dict(exclude_unset=True))
    session.add(api_log)
    session.commit()
    return api_log


def update_api_log(session, api_log_id: int, api_log_update):
    api_log = session.query(ApiLog).filter(ApiLog.id == api_log_id).first()
    if api_log:
        for key, value in api_log_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(api_log, key, value)
        session.commit()
    return api_log


def delete_api_log(session, api_log_id: int):
    api_log = session.query(ApiLog).filter(ApiLog.id == api_log_id).first()
    if api_log:
        session.delete(api_log)
        session.commit()
    return


def get_api_log(session, api_log_id: int):
    api_log = session.query(ApiLog).filter(ApiLog.id == api_log_id).first()
    return api_log
