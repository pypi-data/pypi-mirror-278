"""
@author: fastcodedog
@project: fakeapp
@file: position.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.admin.position import Position
from fastcodedog.test.fakeapp.model.admin.menu import Menu
from fastcodedog.test.fakeapp.model.admin.user import User


def create_position(session, position_create):
    position = Position(**position_create.dict(exclude_unset=True))
    session.add(position)
    session.commit()
    return position


def update_position(session, position_id: int, position_update):
    position = session.query(Position).filter(Position.id == position_id).first()
    if position:
        for key, value in position_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(position, key, value)
        session.commit()
    return position


def delete_position(session, position_id: int):
    position = session.query(Position).filter(Position.id == position_id).first()
    if position:
        session.delete(position)
        session.commit()
    return


def get_position(session, position_id: int):
    position = session.query(Position).filter(Position.id == position_id).first()
    return position


def add_menus_to_position(session, position_id: int, menu_ids: list[int]):
    position = session.query(Position).filter(Position.id == position_id).first()
    menus = session.query(Menu).filter(Menu.id.in_(menu_ids)).all()
    if position:
        for m_ in menus:
            if m_ not in position.menus:
                position.menus.append(m_)
        session.commit()
    return position


def delete_menus_from_position(session, position_id: int, menu_ids: list[int]):
    position = session.query(Position).filter(Position.id == position_id).first()
    menus = session.query(Menu).filter(Menu.id.in_(menu_ids)).all()
    if position:
        for m_ in menus:
            if m_ in position.menus:
                position.menus.remove(m_)
        session.commit()
    return position


def add_users_to_position(session, position_id: int, user_ids: list[int]):
    position = session.query(Position).filter(Position.id == position_id).first()
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    if position:
        for u_ in users:
            if u_ not in position.users:
                position.users.append(u_)
        session.commit()
    return position


def delete_users_from_position(session, position_id: int, user_ids: list[int]):
    position = session.query(Position).filter(Position.id == position_id).first()
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    if position:
        for u_ in users:
            if u_ in position.users:
                position.users.remove(u_)
        session.commit()
    return position
