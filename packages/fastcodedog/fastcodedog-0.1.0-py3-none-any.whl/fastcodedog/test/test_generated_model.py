# -*- coding: utf-8 -*-
"""
@author: hubo
@project: fastframe
@file: test_model
@time: 2024/5/30 8:50
@desc:
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastcodedog.test.fakeapp.model import *

engine = create_engine('postgresql://ccuser:Cc_12345678@192.168.44.128:15432/ccdb')
Session = sessionmaker(bind=engine)
session = Session()


def test_create_table():
    # 需要调用自动创建表来支持创建属性表
    Base.metadata.create_all(engine)


def test_drop_table():
    Base.metadata.drop_all(engine)


def test_recreate_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_cleanr_data():
    session.query(User).delete()
    session.query(Organization).delete()
    session.query(Position).delete()
    session.query(Menu).delete()
    session.query(ApiLog).delete()
    session.query(AttributeSelectItem).delete()
    session.query(AttributeVerification).delete()
    session.query(Attribute).delete()
    session.commit()


def test_create_data():
    # 没有任何关联的单表
    session.add(ApiLog(program='test'))
    # 关联主数据
    attribute = Attribute(code='test', object='test', value_type='string', name='测试属性', default_value='test')
    session.add(attribute)
    session.commit()
    # 创建子数据
    attribute_select_item1 = AttributeSelectItem(text='测试数据', value='test')
    attribute_select_item2 = AttributeSelectItem(text='测试数据2', value='test2')
    attribute.attribute_select_items = [attribute_select_item1, attribute_select_item2]
    session.commit()
    # 指向自身的数据
    parent_organization = Organization(number='test_parent', name='测试父级组织')
    child_organization = Organization(number='test_child', name='测试子级组织')
    child_organization.parent = parent_organization
    session.add(parent_organization)
    session.add(child_organization)
    session.commit()
    # 关联表关联的数据
    user = User(number='testuser', password='123456', name='测试用户')
    user.organizations = [parent_organization, child_organization]
    session.add(user)
    session.commit()


def test_get_data():
    # 没有任何关联的单表
    apilog = session.query(ApiLog).first()
    assert apilog.program == 'test'
    # 关联主数据
    attribute = session.query(Attribute).first()
    assert attribute.name == '测试属性'
    # 指向自身的数据
    parent_organization = session.query(Organization).filter(Organization.number == 'test_parent').first()
    assert parent_organization.name == '测试父级组织'
    assert parent_organization.children[0].parent_id == parent_organization.id
    # 关联表关联的数据
    assert parent_organization.users[0].number == 'testuser'


def test_delete_data():
    # 没有任何关联的单表
    user = session.query(User).first()
    session.delete(user)
    session.commit()
    assert session.query(User).count() == 0
    parent_organization = session.query(Organization).filter(Organization.number == 'test_parent').first()
    assert parent_organization.users == []

# def test_delete_tanent():
#     tenant = session.query(Tenant).first()
#     session.delete(tenant)
#     session.commit()
#     assert session.query(Tenant).count() == 0
