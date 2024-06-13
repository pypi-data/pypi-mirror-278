"""
@author: fastcodedog
@project: fakeapp
@file: attribute_verification.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.define.attribute_verification as crud
from fastcodedog.test.fakeapp.schema.define.attribute_verification import AttributeVerification, AttributeVerificationCreate, AttributeVerificationUpdate
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/attribute_verification', response_model=AttributeVerification, response_model_exclude_none=True)
def create_attribute_verification(attribute_verification_create: AttributeVerificationCreate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.create_attribute_verification(session=session, attribute_verification_create=attribute_verification_create)


@app.put('/attribute_verification/{attribute_verification_id}', response_model=AttributeVerification, response_model_exclude_none=True)
def update_attribute_verification(attribute_verification_id: int, attribute_verification_update: AttributeVerificationUpdate, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.update_attribute_verification(session=session, attribute_verification_id=attribute_verification_id, attribute_verification_update=attribute_verification_update)


@app.delete('/attribute_verification/{attribute_verification_id}')
def delete_attribute_verification(attribute_verification_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_attribute_verification(session=session, attribute_verification_id=attribute_verification_id)


@app.get('/attribute_verification/{attribute_verification_id}', response_model=AttributeVerification, response_model_exclude_none=True)
def get_attribute_verification(attribute_verification_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    return crud.get_attribute_verification(session=session, attribute_verification_id=attribute_verification_id)
