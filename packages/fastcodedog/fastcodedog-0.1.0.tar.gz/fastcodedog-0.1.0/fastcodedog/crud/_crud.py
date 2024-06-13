# -*- coding: utf-8 -*-
import re

from .method_block import MethodBlock
from .param import Param
from ..context.context_instance import ctx_instance
from ..util.case_converter import camel_to_snake


def _create_base_create_function(cls):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    model_param_name = f'{snaked_name}_create'
    schema_class_block = cls.schema.get_schema_class_by_method('create')
    func = MethodBlock(f'create_{snaked_name}', cls, option='create', base_method=True)
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_param_name] = Param(model_param_name, func, schema_class_block=schema_class_block, nullable=False)
    func.content = f"""{snaked_name} = {model_name}(**{snaked_name}_create.dict(exclude_unset=True))
session.add({snaked_name})
session.commit()
return {snaked_name}
"""
    return func


def _create_base_update_function(cls):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    model_id_name = f'{snaked_name}_id'
    model_param_name = f'{snaked_name}_update'
    schema_class_block = cls.schema.get_schema_class_by_method('update')
    func = MethodBlock(f'update_{snaked_name}', cls, option='update', base_method=True)
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_id_name] = Param(model_id_name, func, type='int', nullable=False)
    func.params[model_param_name] = Param(model_param_name, func, schema_class_block=schema_class_block, nullable=False)
    func.content = f"""{snaked_name} = session.query({model_name}).filter({model_name}.id == {model_id_name}).first()
if {snaked_name}:
    for key, value in {snaked_name}_update.dict(exclude_unset=True).items():     # 忽略为None的数据
        setattr({snaked_name}, key, value)
    session.commit()
return {snaked_name}
"""
    return func


def _create_base_delete_function(cls):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    model_id_name = f'{snaked_name}_id'
    func = MethodBlock(f'delete_{snaked_name}', cls, option='delete', base_method=True)
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_id_name] = Param(model_id_name, func, type='int', nullable=False)
    func.content = f"""{snaked_name} = session.query({model_name}).filter({model_name}.id == {model_id_name}).first()
if {snaked_name}:
    session.delete({snaked_name})
    session.commit()
return
"""
    return func


def _create_base_get_function(cls):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    model_id_name = f'{snaked_name}_id'
    func = MethodBlock(f'get_{snaked_name}', cls, option='get', base_method=True)
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_id_name] = Param(model_id_name, func, type='int', nullable=False)
    func.content = f"""{snaked_name} = session.query({model_name}).filter({model_name}.id == {model_id_name}).first()
return {snaked_name}
"""
    return func


def _create_add_relation_function(cls, sub_object):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    back_populates_model = ctx_instance.model_package.models.get(sub_object.back_populate_table.code)
    remote_model_class_name = back_populates_model.class_name
    sub_object_name = sub_object.code
    model_id_name = f'{snaked_name}_id'
    sub_object_model_ids = f'{camel_to_snake(sub_object.back_populate_class_name)}_ids'
    short_object_name = sub_object_name[0] + '_'
    func = MethodBlock(f'add_{sub_object_name}_to_{snaked_name}', cls, sub_object_name=sub_object_name, option='update')
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_id_name] = Param(model_id_name, func, type='int', nullable=False)
    func.params[sub_object_model_ids] = Param(sub_object_model_ids, func, type='list[int]', sub_object=sub_object,
                                              nullable=False)
    func.content = f"""{snaked_name} = session.query({model_name}).filter({model_name}.id == {model_id_name}).first()
{sub_object_name} = session.query({remote_model_class_name}).filter({remote_model_class_name}.id.in_({sub_object_model_ids})).all()
if {snaked_name}:
    for {short_object_name} in {sub_object_name}:
        if {short_object_name} not in {snaked_name}.{sub_object_name}:
            {snaked_name}.{sub_object_name}.append({short_object_name})
    session.commit()
return {snaked_name}
"""
    return func


def _create_delete_relation_function(cls, sub_object):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    back_populates_model = ctx_instance.model_package.models.get(sub_object.back_populate_table.code)
    remote_model_class_name = back_populates_model.class_name
    sub_object_name = sub_object.code
    model_id_name = f'{snaked_name}_id'
    sub_object_model_ids = f'{camel_to_snake(sub_object.back_populate_class_name)}_ids'
    short_object_name = sub_object_name[0] + '_'
    func = MethodBlock(f'delete_{sub_object_name}_from_{snaked_name}', cls, sub_object_name=sub_object_name,
                       option='update')
    func.params['session'] = Param('session', func, nullable=False)
    func.params[model_id_name] = Param(model_id_name, func, type='int', nullable=False)
    func.params[sub_object_model_ids] = Param(sub_object_model_ids, func, type='list[int]', sub_object=sub_object,
                                              nullable=False)
    func.content = f"""{snaked_name} = session.query({model_name}).filter({model_name}.id == {model_id_name}).first()
{sub_object_name} = session.query({remote_model_class_name}).filter({remote_model_class_name}.id.in_({sub_object_model_ids})).all()
if {snaked_name}:
    for {short_object_name} in {sub_object_name}:
        if {short_object_name} in {snaked_name}.{sub_object_name}:
            {snaked_name}.{sub_object_name}.remove({short_object_name})
    session.commit()
return {snaked_name}
"""
    return func


def _create_create_or_update_from_schema_additional(cls, class_block):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    func = MethodBlock(f'{class_block.method}_{snaked_name}_with_{camel_to_snake(class_block.name)}', cls,
                       schema_additional_name=class_block.name, option=class_block.method)
    return func


def _create_query(cls, name, query):
    snaked_name = cls.snaked_name
    model_name = cls.model_class_name
    func = MethodBlock(f'get_{name}', cls, option='get', query_name=name, return_list=True)
    func.params['session'] = Param('session', func, nullable=False)
    for param_name, param in query.parameters.items():
        func.params[param_name] = Param(param_name, func, type=param.type, nullable=param.nullable,
                                        default=param.default, comment=param.description)
    # 查询的固定参数
    func.params['skip'] = Param('skip', func, type='int', default=0)
    func.params['limit'] = Param('limit', func, type='int', default=100)
    func.content = f'query = session.query({model_name})\n'
    for alias_name, alias_value in query.aliases.items():
        func.content += f'{alias_name} = {alias_value}\n'
    for join in query.joins:
        func.content += f'query = query.join({join})\n'
    for outerjoin in query.outerjoins:
        func.content += f'query = query.outerjoin({outerjoin})\n'
    for filter in query.filters:
        params_in_filter = _get_params_in_f_string(filter)
        if not params_in_filter:
            func.content += f'query = query.filter({filter})\n'
            continue
        func.content += f"if {' and '.join([pif + ' is not None:' for pif in params_in_filter])}\n"
        func.content += f'    query = query.filter({filter})\n'
    func.content += f'return query.offset(skip).limit(limit).all()\n'
    return func


def _get_params_in_f_string(f_string):
    # 只是取变量名，有些处理可以粗暴点
    f_s = f_string.replace('{{', '').replace('}}', '')
    return re.findall(r'{(\w+)}', f_s)
