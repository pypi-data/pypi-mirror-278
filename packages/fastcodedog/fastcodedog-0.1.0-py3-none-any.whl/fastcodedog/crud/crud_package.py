# -*- coding: utf-8 -*-
import os

from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.crud.crud import Crud
from fastcodedog.generation.package import Package
from fastcodedog.util.case_converter import camel_to_snake


class CrudPackage(Package):
    def __init__(self):
        self.package = f'{ctx_instance.project_package}.crud'
        self.dir = os.path.join(ctx_instance.project_dir, 'crud')

        # 计算属性
        self.cruds = {}

        for code, schema in ctx_instance.schema_package.schemas.items():
            path = os.path.join(self.dir, schema.model.table.module, self.get_file_name(schema.model.table))
            package = f'{self.package}.{schema.model.table.module}.{camel_to_snake(self.get_class_name(schema.model.table))}'
            crud = Crud(schema, path, package)
            self.cruds[code] = crud

    def save(self):
        for cruds in self.cruds.values():
            cruds.save()
