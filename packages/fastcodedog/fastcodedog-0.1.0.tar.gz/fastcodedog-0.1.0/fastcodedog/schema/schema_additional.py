# -*- coding: utf-8 -*-
from fastcodedog.generation.file import File
from fastcodedog.schema.schema_additional_class_block import SchemaAdditionalClassBlock
from fastcodedog.util.case_converter import snake_to_camel


class SchemaAdditional(File):
    def __init__(self, parent, response_schemas={}, create_schemas={}, update_schemas={}, desc=None):
        self.schema = parent
        path = self.schema.path[:-3] + '_additional.py'
        package = self.schema.package + '_additional'
        super().__init__(path, package, desc=(desc or f'{self.schema.model.name}_additional'))
        self.parent = parent
        self.response_schemas = response_schemas
        self.create_schemas = create_schemas
        self.update_schemas = update_schemas
        self.code = parent.code

        # 需要计算的属性
        # self.class_blocks
        self._init_additional_schemas(base_class_name=self.schema.class_name, package=self.schema.package)
        self._init_import_stmt(self)

    def _init_import_stmt(self, loop_class):
        if hasattr(loop_class, 'schema') and hasattr(loop_class, 'base_class'):
            self.import_stmt.add_import(loop_class.schema.package, loop_class.base_class)
        if hasattr(loop_class, 'class_blocks'):
            for class_block in loop_class.class_blocks.values():
                self._init_import_stmt(class_block)
        if hasattr(loop_class, 'sub_classes'):
            for sub_class in loop_class.sub_classes.values():
                self._init_import_stmt(sub_class)
        if hasattr(loop_class, 'sub_objects'):
            for sub_object in loop_class.sub_objects.values():
                if sub_object.schema_package:
                    self.import_stmt.add_import(sub_object.schema_package, sub_object.class_name)
                if sub_object.is_list:
                    self.import_stmt.add_import('typing', 'List')

    def _init_additional_schemas(self, base_class_name, package):
        for additional_schema_name, additional_schema in self.response_schemas.items():
            class_block = SchemaAdditionalClassBlock(snake_to_camel(additional_schema_name, upper_first=True),
                                                     schema=self.schema,
                                                     method='response',
                                                     additional_schema_element_expressions=additional_schema,
                                                     parent=self)
            self.class_blocks[class_block.name] = class_block
        for additional_schema_name, additional_schema in self.create_schemas.items():
            class_block = SchemaAdditionalClassBlock(snake_to_camel(additional_schema_name, upper_first=True),
                                                     schema=self.schema,
                                                     method='create',
                                                     additional_schema_element_expressions=additional_schema,
                                                     parent=self)
            self.class_blocks[class_block.name] = class_block
        for additional_schema_name, additional_schema in self.update_schemas.items():
            class_block = SchemaAdditionalClassBlock(snake_to_camel(additional_schema_name, upper_first=True),
                                                     schema=self.schema,
                                                     method='update',
                                                     additional_schema_element_expressions=additional_schema,
                                                     parent=self)
            self.class_blocks[class_block.name] = class_block
        ...
