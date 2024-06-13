# -*- coding: utf-8 -*-
import os

from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.package import Package
from .schema import Schema
from ..generation.file import File
from ..generation.function_block import FunctionBlock
from ..generation.param import Param
from ..util.case_converter import camel_to_snake


class SchemaPackage(Package):
    def __init__(self):
        self.package = f'{ctx_instance.project_package}.schema'
        self.dir = os.path.join(ctx_instance.project_dir, 'schema')
        self.schemas = {}  # model类
        self.sample_dynamic_attributes = None

        # 计算属性
        self._init_sample_dynamic_attributes()
        for code, model in ctx_instance.model_package.models.items():
            path = os.path.join(self.dir, model.table.module, self.get_file_name(model.table))
            package = f'{self.package}.{model.table.module}.{camel_to_snake(self.get_class_name(model.table))}'
            schema = Schema(model, path=path, package=package)
            self.schemas[code] = schema

    def _init_sample_dynamic_attributes(self):
        self.sample_dynamic_attributes = File(os.path.join(self.dir, 'callback', 'get_dynamic_attributes.py'),
                                              f'{self.package}.callback.get_dynamic_attributes',
                                              '获取动态属性的例子')
        self.sample_dynamic_attributes.import_stmt.add_import('pydantic', 'Field')
        self.sample_dynamic_attributes.import_stmt.add_import('typing', 'Optional')
        function_block = FunctionBlock('get_dynamic_attributes', self.sample_dynamic_attributes)
        function_block.params['table_name'] = Param('table_name', function_block, type='str', nullable=True)
        function_block.content = "# extra_attribute_sample: Optional[str]= Field(None, exclude_none=True, description='a sample of extra attribute')\n"
        function_block.content += "return {{'extra_attribute_sample': (Optional[str], Field(None, exclude_none=True, description='a sample of extra attribute'))}}\n"
        self.sample_dynamic_attributes.function_blocks['get_dynamic_attributes'] = function_block

    def save(self):
        # 创建callback的例子
        self.sample_dynamic_attributes.save()
        for schema in self.schemas.values():
            schema.save()
