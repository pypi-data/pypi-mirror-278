# -*- coding: utf-8 -*-
import os

from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.package import Package
from fastcodedog.model._base import _Base
from fastcodedog.model.init import Init
from fastcodedog.model.model import Model
from fastcodedog.model.relation_object import RelationObject
from fastcodedog.util.case_converter import camel_to_snake


class ModelPackage(Package):
    def __init__(self):
        self.package = f'{ctx_instance.project_package}.model'
        self.dir = os.path.join(ctx_instance.project_dir, 'model')
        self.models = {}  # model类
        self.relaction_objects = {}  # 关系对象
        self.init = None

        # 计算属性
        if not ctx_instance.base.class_name:
            ctx_instance.base.class_name = 'Base'
            ctx_instance.base.package = f'{self.package}.base'
        if not ctx_instance.diagram:
            raise Exception('请先调用load_diagram方法')
        for table_code, table in ctx_instance.diagram.tables.items():
            path = os.path.join(self.dir, table.module, self.get_file_name(table))
            class_name = self.get_class_name(table)
            package = f'{self.package}.{table.module}.{camel_to_snake(class_name)}'
            if table.is_join_table:
                self.relaction_objects[table_code] = RelationObject(table, path, package)
            else:
                model = Model(table, class_name=class_name, path=path, package=package)
                self.models[table_code] = model

        self.init = Init(path=os.path.join(self.dir, '__init__.py'), package=self.package,
                         models=self.models, relation_objects=self.relaction_objects)

    def save(self):
        self.check_or_create_base()
        for model in self.models.values():
            model.save()
        for relation_object in self.relaction_objects.values():
            relation_object.save()
        self.init.save()

    def check_or_create_base(self):
        path = os.path.join(self.dir, 'base.py')
        if not os.path.exists(path):
            base = _Base(path=path, package=ctx_instance.base.package, desc='基类。一个工程内应该只有一个Base基类')
            base.save()
