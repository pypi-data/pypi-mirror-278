"""
@author: fastcodedog
@project: fakeapp
@file: user.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.admin.user import User
from fastcodedog.test.fakeapp.model.admin.organization import Organization
from fastcodedog.test.fakeapp.model.admin.position import Position


def create_user(session, user_create):
    user = User(**user_create.dict(exclude_unset=True))
    session.add(user)
    session.commit()
    return user


def update_user(session, user_id: int, user_update):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(user, key, value)
        session.commit()
    return user


def delete_user(session, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
    return


def get_user(session, user_id: int):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def add_organizations_to_user(session, user_id: int, organization_ids: list[int]):
    user = session.query(User).filter(User.id == user_id).first()
    organizations = session.query(Organization).filter(Organization.id.in_(organization_ids)).all()
    if user:
        for o_ in organizations:
            if o_ not in user.organizations:
                user.organizations.append(o_)
        session.commit()
    return user


def delete_organizations_from_user(session, user_id: int, organization_ids: list[int]):
    user = session.query(User).filter(User.id == user_id).first()
    organizations = session.query(Organization).filter(Organization.id.in_(organization_ids)).all()
    if user:
        for o_ in organizations:
            if o_ in user.organizations:
                user.organizations.remove(o_)
        session.commit()
    return user


def add_positions_to_user(session, user_id: int, position_ids: list[int]):
    user = session.query(User).filter(User.id == user_id).first()
    positions = session.query(Position).filter(Position.id.in_(position_ids)).all()
    if user:
        for p_ in positions:
            if p_ not in user.positions:
                user.positions.append(p_)
        session.commit()
    return user


def delete_positions_from_user(session, user_id: int, position_ids: list[int]):
    user = session.query(User).filter(User.id == user_id).first()
    positions = session.query(Position).filter(Position.id.in_(position_ids)).all()
    if user:
        for p_ in positions:
            if p_ in user.positions:
                user.positions.remove(p_)
        session.commit()
    return user


def create_user_with_user_create_with_organization():
    ...


def update_user_with_user_update_with_organization():
    ...


def get_base(session, number: str = None, name: str = None, telephone: str = None, email: str = None, state_valid: bool = None, skip: int = 0, limit: int = 100):
    query = session.query(User)
    if number is not None:
        query = query.filter(User.number.like(f'%{number}%'))
    if name is not None:
        query = query.filter(User.name.like(f'%{name}%'))
    if telephone is not None:
        query = query.filter(User.telephone.like(f'%{telephone}%'))
    if email is not None:
        query = query.filter(User.email.like(f'%{email}%'))
    query = query.filter(User.state_valid == state_valid)
    return query.offset(skip).limit(limit).all()


def get_user_by_organization(session, organization_id: int = None, skip: int = 0, limit: int = 100):
    query = session.query(User)
    uo = User.organizations
    query = query.join(uo)
    query = query.filter(uo.id == organization_id)
    return query.offset(skip).limit(limit).all()
