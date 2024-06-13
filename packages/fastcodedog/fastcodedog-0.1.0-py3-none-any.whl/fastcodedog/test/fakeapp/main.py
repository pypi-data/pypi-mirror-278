"""
@author: fastcodedog
@project: fakeapp
@file: main.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastcodedog.test.codes.hello import app as hello_app
from fastcodedog.test.fakeapp.api.admin.user import app as user_app
from fastcodedog.test.fakeapp.api.admin.organization import app as organization_app
from fastcodedog.test.fakeapp.api.admin.position import app as position_app
from fastcodedog.test.fakeapp.api.admin.menu import app as menu_app
from fastcodedog.test.fakeapp.api.operation.api_log import app as api_log_app
from fastcodedog.test.fakeapp.api.define.attribute import app as attribute_app
from fastcodedog.test.fakeapp.api.define.attribute_select_item import app as attribute_select_item_app
from fastcodedog.test.fakeapp.api.define.attribute_verification import app as attribute_verification_app
from fastcodedog.test.fakeapp.api.admin.tenant import app as tenant_app
from fastcodedog.test.fakeapp.api.oauth.oauth import app as oauth_app

app = FastAPI()


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database operation failed: {exc}",
    )
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
app.include_router(hello_app.router)
app.include_router(user_app.router)
app.include_router(organization_app.router)
app.include_router(position_app.router)
app.include_router(menu_app.router)
app.include_router(api_log_app.router)
app.include_router(attribute_app.router)
app.include_router(attribute_select_item_app.router)
app.include_router(attribute_verification_app.router)
app.include_router(tenant_app.router)
app.include_router(oauth_app.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
