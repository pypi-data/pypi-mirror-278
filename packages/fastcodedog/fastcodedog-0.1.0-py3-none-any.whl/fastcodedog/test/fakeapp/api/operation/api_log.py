"""
@author: fastcodedog
@project: fakeapp
@file: api_log.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.operation.api_log as crud
from fastcodedog.test.fakeapp.schema.operation.api_log import ApiLog, ApiLogCreate, ApiLogUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/api_log', response_model=ApiLog, response_model_exclude_none=True)
def create_api_log(api_log_create: ApiLogCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_api_log(session=session, api_log_create=api_log_create)


@app.put('/api_log/{api_log_id}', response_model=ApiLog, response_model_exclude_none=True)
def update_api_log(api_log_id: int, api_log_update: ApiLogUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_api_log(session=session, api_log_id=api_log_id, api_log_update=api_log_update)


@app.delete('/api_log/{api_log_id}')
def delete_api_log(api_log_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_api_log(session=session, api_log_id=api_log_id)


@app.get('/api_log/{api_log_id}', response_model=ApiLog, response_model_exclude_none=True)
def get_api_log(api_log_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_api_log(session=session, api_log_id=api_log_id)
