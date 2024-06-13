"""
@author: fastcodedog
@project: fakeapp
@file: oauth.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改

OAuth2.SECRET_KEY =
OAuth2.EXPIRE_SECONDS = 60*60*2
OAuth2.REDIS_URL = 'redis://localhost:6379/oauth2'

"""
from typing import Annotated
from fastoauth import OAuth2, Token
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastcodedog.test.fakeapp.db import Session, get_session
from fastcodedog.test.fakeapp.model.admin.user import User
from fastcodedog.test.fakeapp.model.admin.tenant import Tenant

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


@app.post('/oauth/token', response_model=Token, response_model_exclude_none=True)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    username = form_data.username
    password = form_data.password
    if username.find('@') == -1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username. Must contain '@'")
    domain = username.split('@')[1]
    username = username.split('@')[0]
    user = session.query(User).join(Tenant, User.tenant_id == Tenant.id).filter(
        User.number == username).filter(User.password == password).filter(Tenant.domain == domain).first()
    if user:
        return OAuth2.create_access_token({"id": user.id, "number": username, "tenant_id": user.tenant_id})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@app.post('/oauth/logout')
def remove_token(token: Annotated[str, Depends(oauth2_scheme)]):
    OAuth2.remove_token(token)
    return {}


@app.post('/oauth/refresh_token', response_model=Token, response_model_exclude_none=True)
def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return OAuth2.refresh_token(token)


@app.get('/oauth/me')
def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return OAuth2.get_token_user(token)
