"""
@author: fastcodedog
@project: fakeapp
@file: attribute.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.define.attribute as crud
from fastcodedog.test.fakeapp.schema.define.attribute import Attribute, AttributeCreate, AttributeUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/attribute', response_model=Attribute, response_model_exclude_none=True)
def create_attribute(attribute_create: AttributeCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_attribute(session=session, attribute_create=attribute_create)


@app.put('/attribute/{attribute_id}', response_model=Attribute, response_model_exclude_none=True)
def update_attribute(attribute_id: int, attribute_update: AttributeUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_attribute(session=session, attribute_id=attribute_id, attribute_update=attribute_update)


@app.delete('/attribute/{attribute_id}')
def delete_attribute(attribute_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_attribute(session=session, attribute_id=attribute_id)


@app.get('/attribute/{attribute_id}', response_model=Attribute, response_model_exclude_none=True)
def get_attribute(attribute_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_attribute(session=session, attribute_id=attribute_id)
