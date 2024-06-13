"""
@author: fastcodedog
@project: fakeapp
@file: position.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.admin.position as crud
from fastcodedog.test.fakeapp.schema.admin.position import Position, PositionCreate, PositionUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/position', response_model=Position, response_model_exclude_none=True)
def create_position(position_create: PositionCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_position(session=session, position_create=position_create)


@app.put('/position/{position_id}', response_model=Position, response_model_exclude_none=True)
def update_position(position_id: int, position_update: PositionUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_position(session=session, position_id=position_id, position_update=position_update)


@app.delete('/position/{position_id}')
def delete_position(position_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_position(session=session, position_id=position_id)


@app.get('/position/{position_id}', response_model=Position, response_model_exclude_none=True)
def get_position(position_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_position(session=session, position_id=position_id)


@app.put('/position/{position_id}/menus', response_model=Position, response_model_exclude_none=True)
def add_menus_to_position(position_id: int, menu_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.add_menus_to_position(session=session, position_id=position_id, menu_ids=menu_ids)


@app.put('/position/{position_id}/menus', response_model=Position, response_model_exclude_none=True)
def delete_menus_from_position(position_id: int, menu_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.delete_menus_from_position(session=session, position_id=position_id, menu_ids=menu_ids)


@app.put('/position/{position_id}/users', response_model=Position, response_model_exclude_none=True)
def add_users_to_position(position_id: int, user_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.add_users_to_position(session=session, position_id=position_id, user_ids=user_ids)


@app.put('/position/{position_id}/users', response_model=Position, response_model_exclude_none=True)
def delete_users_from_position(position_id: int, user_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.delete_users_from_position(session=session, position_id=position_id, user_ids=user_ids)
