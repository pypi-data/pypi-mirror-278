# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.context.query import Query
from fastcodedog.crud._crud import (_create_base_create_function, _create_base_update_function,
                                    _create_base_delete_function, _create_base_get_function,
                                    _create_add_relation_function, _create_delete_relation_function,
                                    _create_create_or_update_from_schema_additional, _create_query)
from fastcodedog.generation.file import File
from fastcodedog.model.sub_object import SubObject
from fastcodedog.util.case_converter import camel_to_snake


class Crud(File):
    def __init__(self, schema, path, package, desc=None):
        super().__init__(path, package, desc)

        self.code = schema.code
        self.schema = schema

        # 全局使用的临时变量
        self.snaked_name = camel_to_snake(self.schema.class_name)
        self.model_class_name = schema.model.class_name

        # 计算的属性
        self.schema_additional = ctx_instance.schema_additional_package.shcema_additionals.get(self.code)
        # self.function_blocks

        # 计算属性
        self._init_functions()
        self._init_import_stmt()

    def _init_functions(self):
        create_function = _create_base_create_function(self)
        self.function_blocks[create_function.name] = create_function
        update_function = _create_base_update_function(self)
        self.function_blocks[update_function.name] = update_function
        delete_function = _create_base_delete_function(self)
        self.function_blocks[delete_function.name] = delete_function
        get_function = _create_base_get_function(self)
        self.function_blocks[get_function.name] = get_function
        self._init_relation_object_functiion()
        self._init_create_or_update_from_schema_additionals()
        self._init_queries()

    def _init_queries(self):
        queries = ctx_instance.queries.get(self.code, {})
        for name, json in queries.items():
            query = Query(json)
            func = _create_query(self, name, query)
            self.function_blocks[func.name] = func

    def _init_create_or_update_from_schema_additionals(self):
        if not self.schema_additional:
            return
        for class_block in self.schema_additional.class_blocks.values():
            if class_block.method in ['create', 'update']:
                func = _create_create_or_update_from_schema_additional(self, class_block)
                self.function_blocks[func.name] = func

    def _init_relation_object_functiion(self):
        for sub_object in self.schema.model.class_stmt.sub_objects.values():
            if not isinstance(sub_object, SubObject):
                continue
            if not sub_object.refer_to_join_table:  # 只处理多对多关联
                continue
            add_relation_function = _create_add_relation_function(self, sub_object)
            self.function_blocks[add_relation_function.name] = add_relation_function
            delete_relation_function = _create_delete_relation_function(self, sub_object)
            self.function_blocks[delete_relation_function.name] = delete_relation_function

    def _init_import_stmt(self):
        self.import_stmt.add_import(self.schema.model.package, self.schema.model.class_name)
        for func_block in self.function_blocks.values():
            for param in func_block.params.values():
                if param.sub_object:
                    back_populates_model = ctx_instance.model_package.models.get(
                        param.sub_object.back_populate_table.code)
                    self.import_stmt.add_import(back_populates_model.package, back_populates_model.class_name)
