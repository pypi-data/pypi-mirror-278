"""
@author: fastcodedog
@project: fakeapp
@file: attribute_verification.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.define.attribute_verification import AttributeVerification


def create_attribute_verification(session, attribute_verification_create):
    attribute_verification = AttributeVerification(**attribute_verification_create.dict(exclude_unset=True))
    session.add(attribute_verification)
    session.commit()
    return attribute_verification


def update_attribute_verification(session, attribute_verification_id: int, attribute_verification_update):
    attribute_verification = session.query(AttributeVerification).filter(
        AttributeVerification.id == attribute_verification_id).first()
    if attribute_verification:
        for key, value in attribute_verification_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(attribute_verification, key, value)
        session.commit()
    return attribute_verification


def delete_attribute_verification(session, attribute_verification_id: int):
    attribute_verification = session.query(AttributeVerification).filter(
        AttributeVerification.id == attribute_verification_id).first()
    if attribute_verification:
        session.delete(attribute_verification)
        session.commit()
    return


def get_attribute_verification(session, attribute_verification_id: int):
    attribute_verification = session.query(AttributeVerification).filter(
        AttributeVerification.id == attribute_verification_id).first()
    return attribute_verification
