# -*- coding: utf-8 -*-
from fastcodedog.util.indent import add_indent
from .generationbase import GenerationBase


class FunctionBlock(GenerationBase):
    def __init__(self, name, parent, params=None):
        self.name = name
        self.parent = parent  # 指向父级，一般是FileStmt或者ClassStmt
        self.params = params if params else {}  # 方法的入参
        self.content = '...\n'

    def serialize(self, indent=''):
        serialized_params = []
        for param in self.params.values():
            if not param.nullable:
                serialized_params.append(param.serialize().strip())
        for param in self.params.values():
            if param.nullable:
                serialized_params.append(param.serialize().strip())
        content = f'def {self.name}({", ".join(serialized_params)}):\n'
        content += add_indent(self.content, '    ')
        return add_indent(content, indent)
