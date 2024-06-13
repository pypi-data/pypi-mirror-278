"""
@author: fastcodedog
@project: fakeapp
@file: user.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.admin.user as crud
from fastcodedog.test.fakeapp.schema.admin.user import User, UserCreate, UserUpdate
from typing import Optional, Union, Annotated
from fastcodedog.test.fakeapp.schema.admin.user_additional import UserWithOrganization, UserWithOrganizationAndPosition, UserWithPositionMenu, UserWithMenu, UserWithUserMenu, UserCreateWithOrganization, UserUpdateWithOrganization
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
ALL_USER_RESPONSE_MODEL = Union[User, UserWithOrganization,
                                UserWithOrganizationAndPosition, UserWithPositionMenu, UserWithMenu, UserWithUserMenu]
ALL_USER_LIST_RESPONSE_MODEL = Union[list[User], list[UserWithOrganization],
                                     list[UserWithOrganizationAndPosition], list[UserWithPositionMenu], list[UserWithMenu], list[UserWithUserMenu]]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


def validate_user_response_model(response_model: str = Query(None, description="指定返回的数据类型，默认为'user'", enum=['user', 'user_with_organization', 'user_with_organization_and_position', 'user_with_position_menu', 'user_with_menu', 'user_with_user_menu'])):
    if response_model and response_model not in ['user', 'user_with_organization', 'user_with_organization_and_position', 'user_with_position_menu', 'user_with_menu', 'user_with_user_menu']:
        raise HTTPException(status_code=400,
                            detail="Invalid response_model. Must in 'user', 'user_with_organization', 'user_with_organization_and_position', 'user_with_position_menu', 'user_with_menu', 'user_with_user_menu'.")
    if response_model == 'user':
        return User
    if response_model == 'user_with_organization':
        return UserWithOrganization
    if response_model == 'user_with_organization_and_position':
        return UserWithOrganizationAndPosition
    if response_model == 'user_with_position_menu':
        return UserWithPositionMenu
    if response_model == 'user_with_menu':
        return UserWithMenu
    if response_model == 'user_with_user_menu':
        return UserWithUserMenu
    return User


@app.post('/user', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def create_user(user_create: UserCreate, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.create_user(session=session, user_create=user_create))


@app.put('/user/{user_id}', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def update_user(user_id: int, user_update: UserUpdate, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.update_user(session=session, user_id=user_id, user_update=user_update))


@app.delete('/user/{user_id}')
def delete_user(user_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_user(session=session, user_id=user_id)


@app.get('/user/{user_id}', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def get_user(user_id: int, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.get_user(session=session, user_id=user_id))


@app.put('/user/{user_id}/organizations', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def add_organizations_to_user(user_id: int, organization_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.add_organizations_to_user(session=session, user_id=user_id, organization_ids=organization_ids))


@app.put('/user/{user_id}/organizations', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def delete_organizations_from_user(user_id: int, organization_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.delete_organizations_from_user(session=session, user_id=user_id, organization_ids=organization_ids))


@app.put('/user/{user_id}/positions', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def add_positions_to_user(user_id: int, position_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.add_positions_to_user(session=session, user_id=user_id, position_ids=position_ids))


@app.put('/user/{user_id}/positions', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def delete_positions_from_user(user_id: int, position_ids: list[int], token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.delete_positions_from_user(session=session, user_id=user_id, position_ids=position_ids))


@app.post('/user/user_create_with_organization', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def create_user_with_user_create_with_organization(token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.create_user_with_user_create_with_organization())


@app.put('/user/user_update_with_organization', response_model=ALL_USER_RESPONSE_MODEL, response_model_exclude_none=True)
def update_user_with_user_update_with_organization(token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.update_user_with_user_update_with_organization())


@app.get('/users/base', response_model=ALL_USER_LIST_RESPONSE_MODEL, response_model_exclude_none=True)
def get_base(token: Annotated[str, Depends(oauth2_scheme)], number: str = None, name: str = None, telephone: str = None, email: str = None, state_valid: bool = None, skip: int = 0, limit: int = 100, response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return [response_model.from_orm(user) for user in crud.get_base(session=session, number=number, name=name, telephone=telephone, email=email, state_valid=state_valid, skip=skip, limit=limit)]


@app.get('/users/user_by_organization', response_model=ALL_USER_LIST_RESPONSE_MODEL, response_model_exclude_none=True)
def get_user_by_organization(token: Annotated[str, Depends(oauth2_scheme)], organization_id: int = None, skip: int = 0, limit: int = 100, response_model: BaseModel = Depends(validate_user_response_model), session: Session = Depends(get_session)):
    return [response_model.from_orm(user) for user in crud.get_user_by_organization(session=session, organization_id=organization_id, skip=skip, limit=limit)]
