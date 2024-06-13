"""
@author: fastcodedog
@project: fakeapp
@file: menu.py
@time: 2024-06-12 15:34:21
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.admin.menu import Menu
from fastcodedog.test.fakeapp.model.admin.position import Position


def create_menu(session, menu_create):
    menu = Menu(**menu_create.dict(exclude_unset=True))
    session.add(menu)
    session.commit()
    return menu


def update_menu(session, menu_id: int, menu_update):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        for key, value in menu_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(menu, key, value)
        session.commit()
    return menu


def delete_menu(session, menu_id: int):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    if menu:
        session.delete(menu)
        session.commit()
    return


def get_menu(session, menu_id: int):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    return menu


def add_positions_to_menu(session, menu_id: int, position_ids: list[int]):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    positions = session.query(Position).filter(Position.id.in_(position_ids)).all()
    if menu:
        for p_ in positions:
            if p_ not in menu.positions:
                menu.positions.append(p_)
        session.commit()
    return menu


def delete_positions_from_menu(session, menu_id: int, position_ids: list[int]):
    menu = session.query(Menu).filter(Menu.id == menu_id).first()
    positions = session.query(Position).filter(Position.id.in_(position_ids)).all()
    if menu:
        for p_ in positions:
            if p_ in menu.positions:
                menu.positions.remove(p_)
        session.commit()
    return menu
