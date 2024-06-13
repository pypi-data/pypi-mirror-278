"""
@author: fastcodedog
@project: fakeapp
@file: tenant.py
@time: 2024-06-12 16:56:20
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.admin.tenant as crud
from fastcodedog.test.fakeapp.schema.admin.tenant import Tenant, TenantCreate, TenantUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/tenant', response_model=Tenant, response_model_exclude_none=True)
def create_tenant(tenant_create: TenantCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_tenant(session=session, tenant_create=tenant_create)


@app.put('/tenant/{tenant_id}', response_model=Tenant, response_model_exclude_none=True)
def update_tenant(tenant_id: int, tenant_update: TenantUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_tenant(session=session, tenant_id=tenant_id, tenant_update=tenant_update)


@app.delete('/tenant/{tenant_id}')
def delete_tenant(tenant_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_tenant(session=session, tenant_id=tenant_id)


@app.get('/tenant/{tenant_id}', response_model=Tenant, response_model_exclude_none=True)
def get_tenant(tenant_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_tenant(session=session, tenant_id=tenant_id)
