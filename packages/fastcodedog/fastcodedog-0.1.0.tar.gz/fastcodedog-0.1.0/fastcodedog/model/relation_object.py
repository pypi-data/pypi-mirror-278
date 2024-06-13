# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.file import File
from fastcodedog.generation.package import Package
from fastcodedog.generation.variable import Variable
from fastcodedog.util.case_converter import camel_to_snake
from fastcodedog.util.type_converter import database_type_to_sqlalchemy_type


class RelationObject(File):
    class ObjectStmt(Variable):
        def __init__(self, table):
            super().__init__(camel_to_snake(Package.get_class_name(table)), table)

        def serialize(self):
            table = self.parent
            (column1, column2) = table.columns.values()
            return f"""{self.code} = Table('{table.code}', Base.metadata,
  Column('{column1.code}', {database_type_to_sqlalchemy_type(column1.data_type)[0]},
         ForeignKey('{column1.foreign_table.code}.{column1.foreign_column.code}', ondelete='CASCADE'), primary_key={column1.primary_key}),
  Column('{column2.code}', {database_type_to_sqlalchemy_type(column2.data_type)[0]},
         ForeignKey('{column2.foreign_table.code}.{column2.foreign_column.code}', ondelete='CASCADE'), primary_key={column2.primary_key})
  )
"""

    def __init__(self, table, path, package, desc=None):
        super().__init__(path, package, desc=(desc or table.name))
        self.table = table
        self._init_import_stmt()
        object_stmt = self.ObjectStmt(table)
        self.variables[object_stmt.code] = self.ObjectStmt(table)

    def _init_import_stmt(self):
        self.import_stmt.add_import('sqlalchemy', 'Column')
        self.import_stmt.add_import('sqlalchemy', 'ForeignKey')
        for column in self.table.columns.values():
            self.import_stmt.add_import('sqlalchemy', database_type_to_sqlalchemy_type(column.data_type)[0])
        self.import_stmt.add_import('sqlalchemy', 'Table')
        self.import_stmt.add_import(ctx_instance.base.package, ctx_instance.base.class_name)
