# -*- coding: utf-8 -*-
from fastcodedog.generation.function_block import FunctionBlock


class MethodBlock(FunctionBlock):
    def __init__(self, name, parent, option=None, base_method=False, sub_object_name=None, schema_additional_name=None,
                 query_name=None, return_list=False, params=None):
        super().__init__(name, parent, params)
        self.option = option  # create, update, delete, get
        self.base_method = base_method
        self.sub_object_name = sub_object_name
        self.schema_additional_name = schema_additional_name
        self.query_name = query_name
        self.return_list = return_list
