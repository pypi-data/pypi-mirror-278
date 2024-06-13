# -*- coding: utf-8 -*-
from fastcodedog.generation.variable import Variable


class UniqueStmt(Variable):
    def __init__(self, code, parent, unique_keys):
        super().__init__(code, parent)
        self.unique_keys = unique_keys  # {unique_key: [column1, column2]}

    def serialize(self):
        unique_constraints = []
        for key, columns in self.unique_keys.items():
            if len(columns) == 0:
                raise Exception(f'{self.parent.code} unique_key {key} should not be empty')
            unique_constraints.append(f'UniqueConstraint({", ".join([column.code for column in columns])})')
        return f'{self.code} = ({", ".join(unique_constraints)},)\n'
