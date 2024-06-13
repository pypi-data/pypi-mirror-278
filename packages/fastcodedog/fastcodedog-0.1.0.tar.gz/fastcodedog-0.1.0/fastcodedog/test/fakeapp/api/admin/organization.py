"""
@author: fastcodedog
@project: fakeapp
@file: organization.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.admin.organization as crud
from fastcodedog.test.fakeapp.schema.admin.organization import Organization, OrganizationCreate, OrganizationUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/organization', response_model=Organization, response_model_exclude_none=True)
def create_organization(organization_create: OrganizationCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_organization(session=session, organization_create=organization_create)


@app.put('/organization/{organization_id}', response_model=Organization, response_model_exclude_none=True)
def update_organization(organization_id: int, organization_update: OrganizationUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_organization(session=session, organization_id=organization_id, organization_update=organization_update)


@app.delete('/organization/{organization_id}')
def delete_organization(organization_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_organization(session=session, organization_id=organization_id)


@app.get('/organization/{organization_id}', response_model=Organization, response_model_exclude_none=True)
def get_organization(organization_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_organization(session=session, organization_id=organization_id)


@app.put('/organization/{organization_id}/users', response_model=Organization, response_model_exclude_none=True)
def add_users_to_organization(organization_id: int, user_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.add_users_to_organization(session=session, organization_id=organization_id, user_ids=user_ids)


@app.put('/organization/{organization_id}/users', response_model=Organization, response_model_exclude_none=True)
def delete_users_from_organization(organization_id: int, user_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.delete_users_from_organization(session=session, organization_id=organization_id, user_ids=user_ids)
