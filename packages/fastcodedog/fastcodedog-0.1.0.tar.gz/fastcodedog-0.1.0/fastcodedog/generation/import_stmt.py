# -*- coding: utf-8 -*-

from fastcodedog.util.indent import add_indent
from .generationbase import GenerationBase


class _ImportExpression(GenerationBase):
    def __init__(self, import_, as_=None):
        self.import_ = import_
        self.as_ = as_

    def serialize(self):
        if self.as_:
            return f'{self.import_} as {self.as_}'
        return self.import_


class _FromExpression:
    def __init__(self, from_):
        self.from_ = from_
        self.import_expressions = {}

    def serialize(self):
        if self.from_ and self.from_ != '':
            return f'from {self.from_} import {", ".join([import_expression.serialize() for import_expression in self.import_expressions.values()])}\n'
        return f'import {", ".join([import_expression.serialize() for import_expression in self.import_expressions.values()])}\n'

    def add_import(self, import_, as_):
        if import_ not in self.import_expressions:
            self.import_expressions[import_] = _ImportExpression(import_, as_)
        elif self.import_expressions[import_].as_ and as_ and self.import_expressions[import_].as_ != as_:
            raise ValueError(
                f'import语句别名冲突：import {import_} as {as_}，已经存在的别名{self.import_expressions[import_].as_}')
        else:
            self.import_expressions[import_].as_ = as_


class ImportStmt:
    """
    一个ImportStmt包含多个FromStmt
    每个FromStmt，from部分相同可以包含多个import
    每个import可以包含一个as，如果传入多个相同的import但是as并且不相同，会报错
    """

    def __init__(self):
        self.from_expressions = {}

    def serialize(self, indent=''):
        result = ''
        for from_ in self.from_expressions.values():
            result += from_.serialize()
        return add_indent(result, indent)

    def add_import(self, from_, import_, as_=None):
        if from_ is None:
            from_ = ''  # 方便加入到电子里
        if from_ not in self.from_expressions:
            self.from_expressions[from_] = _FromExpression(from_)
        self.from_expressions[from_].add_import(import_, as_)

    def load_import(self, json):
        self.add_import(json.get('from'), json.get('import'), json.get('as'))
