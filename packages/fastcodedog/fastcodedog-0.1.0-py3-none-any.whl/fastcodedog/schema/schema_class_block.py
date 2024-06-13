# -*- coding: utf-8 -*-
from fastcodedog.generation.classs_block import ClassBlock
from fastcodedog.util.indent import add_indent


class SchemaClassBlock(ClassBlock):
    def __init__(self, name, base_class, parent, method):
        super().__init__(name, base_class, parent)
        self.method = method
        self.config_class = None

    def serialize(self, indent=''):
        content = super().serialize(indent)
        if self.config_class:
            content += add_indent(self.config_class.serialize(), '    ')
        return content
