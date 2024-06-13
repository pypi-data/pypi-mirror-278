"""
@author: fastcodedog
@project: fakeapp
@file: menu.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.admin.menu as crud
from fastcodedog.test.fakeapp.schema.admin.menu import Menu, MenuCreate, MenuUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/menu', response_model=Menu, response_model_exclude_none=True)
def create_menu(menu_create: MenuCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_menu(session=session, menu_create=menu_create)


@app.put('/menu/{menu_id}', response_model=Menu, response_model_exclude_none=True)
def update_menu(menu_id: int, menu_update: MenuUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_menu(session=session, menu_id=menu_id, menu_update=menu_update)


@app.delete('/menu/{menu_id}')
def delete_menu(menu_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_menu(session=session, menu_id=menu_id)


@app.get('/menu/{menu_id}', response_model=Menu, response_model_exclude_none=True)
def get_menu(menu_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_menu(session=session, menu_id=menu_id)


@app.put('/menu/{menu_id}/positions', response_model=Menu, response_model_exclude_none=True)
def add_positions_to_menu(menu_id: int, position_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.add_positions_to_menu(session=session, menu_id=menu_id, position_ids=position_ids)


@app.put('/menu/{menu_id}/positions', response_model=Menu, response_model_exclude_none=True)
def delete_positions_from_menu(menu_id: int, position_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.delete_positions_from_menu(session=session, menu_id=menu_id, position_ids=position_ids)
