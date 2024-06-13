"""
@author: fastcodedog
@project: fakeapp
@file: organization.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.admin.organization import Organization
from fastcodedog.test.fakeapp.model.admin.user import User


def create_organization(session, organization_create):
    organization = Organization(**organization_create.dict(exclude_unset=True))
    session.add(organization)
    session.commit()
    return organization


def update_organization(session, organization_id: int, organization_update):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if organization:
        for key, value in organization_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(organization, key, value)
        session.commit()
    return organization


def delete_organization(session, organization_id: int):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if organization:
        session.delete(organization)
        session.commit()
    return


def get_organization(session, organization_id: int):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    return organization


def add_users_to_organization(session, organization_id: int, user_ids: list[int]):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    if organization:
        for u_ in users:
            if u_ not in organization.users:
                organization.users.append(u_)
        session.commit()
    return organization


def delete_users_from_organization(session, organization_id: int, user_ids: list[int]):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    if organization:
        for u_ in users:
            if u_ in organization.users:
                organization.users.remove(u_)
        session.commit()
    return organization
