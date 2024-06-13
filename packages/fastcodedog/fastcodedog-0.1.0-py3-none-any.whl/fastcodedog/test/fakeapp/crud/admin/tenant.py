"""
@author: fastcodedog
@project: fakeapp
@file: tenant.py
@time: 2024-06-12 16:56:19
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
from fastcodedog.test.fakeapp.model.admin.tenant import Tenant


def create_tenant(session, tenant_create):
    tenant = Tenant(**tenant_create.dict(exclude_unset=True))
    session.add(tenant)
    session.commit()
    return tenant


def update_tenant(session, tenant_id: int, tenant_update):
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        for key, value in tenant_update.dict(exclude_unset=True).items():     # 忽略为None的数据
            setattr(tenant, key, value)
        session.commit()
    return tenant


def delete_tenant(session, tenant_id: int):
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        session.delete(tenant)
        session.commit()
    return


def get_tenant(session, tenant_id: int):
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    return tenant
