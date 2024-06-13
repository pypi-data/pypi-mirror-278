# -*- coding: utf-8 -*-
from .contextbase import ContextBase


class Schema(ContextBase):
    class AliasGenerator(ContextBase):
        def __init__(self):
            self.import_stmt = {}
            self.function = None

    class DynamicAttributesFunction(ContextBase):
        def __init__(self):
            self.import_stmt = {}
            self.function = None

    class DefaultValue(ContextBase):
        def __init__(self):
            self.import_stmt = None
            self.value_expression = None

    def __init__(self):
        self.no_response_attributes = []
        self.no_set_attributes = []
        self.alias_generator = Schema.AliasGenerator()
        self.dynamic_attributes_function = Schema.DynamicAttributesFunction()
        self.default_values = {}

    @staticmethod
    def new_instance(config_name):
        if config_name == 'default_values':
            return Schema.DefaultValue()
        return ContextBase.new_instance(config_name)
