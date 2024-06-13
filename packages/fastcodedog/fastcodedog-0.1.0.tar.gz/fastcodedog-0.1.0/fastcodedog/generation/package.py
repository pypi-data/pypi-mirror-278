# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.util.case_converter import snake_to_camel, camel_to_snake


class Package:
    def save(self):
        raise NotImplementedError

    @staticmethod
    def get_class_name(table):
        name = ctx_instance.modules.specified_classe_names.get(table.code) or table.code[len(table.module):]
        return snake_to_camel(name)

    @staticmethod
    def get_file_name(table):
        class_name = Package.get_class_name(table)
        return f'{camel_to_snake(class_name)}.py'
