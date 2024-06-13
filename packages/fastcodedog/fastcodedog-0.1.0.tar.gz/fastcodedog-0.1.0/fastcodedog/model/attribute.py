# -*- coding: utf-8 -*-
from fastcodedog.generation.variable import Variable
from fastcodedog.util.type_converter import database_type_to_sqlalchemy_type


class Attribute(Variable):
    def __init__(self, column, parent, comment=None):
        super().__init__(column.code, parent, column.data_type, comment or column.code)
        self.column = column
        self.code = column.code

        # 需要计算的属性
        self.type_with_length = None

        self.type, self.type_with_length = database_type_to_sqlalchemy_type(self.column.data_type, self.column.length)

    def serialize(self):
        args = [self.type_with_length]
        if self.column.primary_key:
            args.append('primary_key=True')
        if self.column.foreign_table:
            args.append('ForeignKey(\'%s.%s\')' % (self.column.foreign_table.code, self.column.foreign_column.code))
        # unique
        if self.column.unique:
            args.append('unique=True')
        # nullable
        if not self.column.primary_key and not self.column.nullable:
            args.append('nullable=False')
        # 备注
        # 还没有好的办法，解决备注带来的格式混乱问题。先用name代替备注
        if self.column.name and self.column.name != '':
            args.append('comment=\'%s\'' % self.column.name.replace('\'', '\\\'').replace('\n', '\\n'))

        return f'{self.code} = Column({", ".join(args)})\n'
