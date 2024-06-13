# -*- coding: utf-8 -*-
from fastcodedog.generation.variable import Variable


class Param(Variable):
    # 方法的参数
    def serialize(self):
        result = self.code
        if self.type:
            result += f': {self.type}'
        if self.default:
            result += f' = {self.default}'
        elif self.nullable:
            result += ' = None'
        return result
