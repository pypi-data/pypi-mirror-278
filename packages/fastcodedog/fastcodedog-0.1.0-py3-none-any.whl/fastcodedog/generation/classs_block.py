# -*- coding: utf-8 -*-
from fastcodedog.util.indent import add_indent
from .generationbase import GenerationBase


class ClassBlock(GenerationBase):
    """这里给出一个指引，需要的数据和生成代码的逻辑都需要重新定义"""

    def __init__(self, name, base_class, parent):
        self.name = name
        self.base_class = base_class
        self.parent = parent  # 指向父级，一般是FileStmt或者ClassStmt
        self.attributes = {}
        self.sub_objects = {}
        self.functions = {}
        self.sub_classes = {}

    def serialize(self, indent=''):
        content = f'class {self.name}' + (f'({self.base_class})' if self.base_class else '') + ':\n'
        for sub_class in self.sub_classes.values():
            content += add_indent(sub_class.serialize(), '    ')
            content += '\n'
        for attribute in self.attributes.values():
            content += add_indent(attribute.serialize(), '    ')
        if self.attributes:
            content += '\n'
        for sub_object in self.sub_objects.values():
            content += add_indent(sub_object.serialize(), '    ')
        if self.sub_objects:
            content += '\n'
        for function in self.functions.values():
            content += add_indent(function.serialize(), '    ')
        if not self.sub_classes and not self.attributes and not self.sub_objects and not self.functions:
            content += '    pass\n'

        return add_indent(content, indent)
