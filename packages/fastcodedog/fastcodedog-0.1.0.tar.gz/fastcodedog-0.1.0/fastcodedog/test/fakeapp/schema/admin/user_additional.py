"""
@author: fastcodedog
@project: fakeapp
@file: user_additional.py
@time: 2024-06-12 15:34:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
schema_additional
"""
from fastcodedog.test.fakeapp.schema.admin.user import User, UserCreate, UserUpdate
from fastcodedog.test.fakeapp.schema.admin.organization import Organization, OrganizationCreate, OrganizationUpdate
from typing import List
from fastcodedog.test.fakeapp.schema.admin.position import Position
from fastcodedog.test.fakeapp.schema.admin.menu import Menu


class UserWithOrganization(User):
    organizations: List[Organization] = []


class UserWithOrganizationAndPosition(User):
    organizations: List[Organization] = []
    positions: List[Position] = []


class UserWithPositionMenu(User):
    class _Position(Position):
        menus: List[Menu] = []

    positions: List[_Position] = []


class UserWithMenu(User):
    class _Position(Position):
        menus: List[Menu] = []

    menus: List[_Position] = []


class UserWithUserMenu(User):
    class _Position(Position):
        menus: List[Menu] = []

    user_menus: List[_Position] = []


class UserCreateWithOrganization(UserCreate):
    organizations: List[OrganizationCreate] = []


class UserUpdateWithOrganization(UserUpdate):
    organizations: List[OrganizationUpdate] = []
