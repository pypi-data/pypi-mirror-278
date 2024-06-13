# -*- coding: utf-8 -*-
from .generationbase import GenerationBase


class Variable(GenerationBase):
    def __init__(self, code, parent, type=None, nullable=True, default=None, comment=None):
        self.code = code
        self.parent = parent  # 指向父级，一般是FileStmt、ClassStmt、FunctionStmt
        self.type = type
        self.nullable = nullable  # 是否可以为None
        self.default = default  # 默认值
        self.comment = comment

    def serialize(self, force_serialize_type=False):
        content = f'{self.code}'
        if self.type and (
                force_serialize_type or self.type in ['bool', 'str', 'int', 'float', 'datetime', 'date', 'time']):
            content += f': {self.type}'  # 并不是所有都需要返回type
        default_value = self.get_default_value_with_fmt()
        if default_value:
            content += f' = {default_value}'
        return content + '\n'

    def get_default_value_with_fmt(self):
        if self.default and self.type in ['bool', 'int', 'float', 'function', 'list', 'dict', 'set', 'Union']:
            return str(self.default)
        if self.default and isinstance(self.default, str):
            # 实际上是调用了一个函数
            if self.default.endswith(')') and self.default.count('(') == self.default.count(')'):
                return self.default
            return f"'{self.default}'"
        if self.default is not None:
            return str(self.default)
        if self.nullable:
            return 'None'
