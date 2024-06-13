"""
@author: fastcodedog
@project: fakeapp
@file: attribute_select_item.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
from fastcodedog.test.fakeapp.model.base import Base
from fastcodedog.test.fakeapp.db import Session, get_session
import fastcodedog.test.fakeapp.crud.define.attribute_select_item as crud
from fastcodedog.test.fakeapp.schema.define.attribute_select_item import AttributeSelectItem, AttributeSelectItemCreate, AttributeSelectItemUpdate
from fastcodedog.test.fakeapp.schema.define.attribute_select_item_additional import SelectItemWithAttribute
from typing import Union, Annotated
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
ALL_ATTRIBUTESELECTITEM_RESPONSE_MODEL = Union[AttributeSelectItem, SelectItemWithAttribute]
ALL_ATTRIBUTESELECTITEM_LIST_RESPONSE_MODEL = Union[list[AttributeSelectItem], list[SelectItemWithAttribute]]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/oauth/token')


def validate_attributeselectitem_response_model(response_model: str = Query(None, description="指定返回的数据类型，默认为'attribute_select_item'", enum=['attribute_select_item', 'select_item_with_attribute'])):
    if response_model and response_model not in ['attribute_select_item', 'select_item_with_attribute']:
        raise HTTPException(status_code=400,
                            detail="Invalid response_model. Must in 'attribute_select_item', 'select_item_with_attribute'.")
    if response_model == 'attribute_select_item':
        return AttributeSelectItem
    if response_model == 'select_item_with_attribute':
        return SelectItemWithAttribute
    return AttributeSelectItem


@app.post('/attribute_select_item', response_model=ALL_ATTRIBUTESELECTITEM_RESPONSE_MODEL, response_model_exclude_none=True)
def create_attribute_select_item(attribute_select_item_create: AttributeSelectItemCreate, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_attributeselectitem_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.create_attribute_select_item(session=session, attribute_select_item_create=attribute_select_item_create))


@app.put('/attribute_select_item/{attribute_select_item_id}', response_model=ALL_ATTRIBUTESELECTITEM_RESPONSE_MODEL, response_model_exclude_none=True)
def update_attribute_select_item(attribute_select_item_id: int, attribute_select_item_update: AttributeSelectItemUpdate, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_attributeselectitem_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.update_attribute_select_item(session=session, attribute_select_item_id=attribute_select_item_id, attribute_select_item_update=attribute_select_item_update))


@app.delete('/attribute_select_item/{attribute_select_item_id}')
def delete_attribute_select_item(attribute_select_item_id: int, token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    crud.delete_attribute_select_item(session=session, attribute_select_item_id=attribute_select_item_id)


@app.get('/attribute_select_item/{attribute_select_item_id}', response_model=ALL_ATTRIBUTESELECTITEM_RESPONSE_MODEL, response_model_exclude_none=True)
def get_attribute_select_item(attribute_select_item_id: int, token: Annotated[str, Depends(oauth2_scheme)], response_model: BaseModel = Depends(validate_attributeselectitem_response_model), session: Session = Depends(get_session)):
    return response_model.from_orm(crud.get_attribute_select_item(session=session, attribute_select_item_id=attribute_select_item_id))
