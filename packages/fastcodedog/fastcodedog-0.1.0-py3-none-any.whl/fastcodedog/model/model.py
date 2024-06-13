# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.classs_block import ClassBlock
from fastcodedog.generation.file import File
from fastcodedog.generation.variable import Variable
from fastcodedog.model.attribute import Attribute
from fastcodedog.model.sub_object import SubObject
from fastcodedog.model.unique_stmt import UniqueStmt


class Model(File):
    def __init__(self, table, class_name, path, package, desc=None):
        super().__init__(path, package, desc=(desc or table.name))
        self.table = table
        self.class_name = class_name
        self.code = table.code

        # 计算出的属性
        self.class_stmt = ClassBlock(class_name, ctx_instance.base.class_name, self)
        self._init_attributes()
        # self.import_stmt      # 继承父类
        self.class_blocks[class_name] = self.class_stmt  # 继承父类
        # self.unique_stmts = {}  # UniqueStmt()
        # self.sub_objects = {}

        # 各种初始化
        self._init_attributes()
        self._init_unique_stmts()
        self._init_sub_objects()
        self._init_import_stmt()

    def _init_sub_objects(self):
        if self.table.is_join_table:
            return
        for reference in self.table.child_side_references:
            sub_object = SubObject(None, reference=reference, parent=self, parent_side=False)
            self.class_stmt.sub_objects[sub_object.code] = sub_object
        for reference in self.table.parent_side_references:
            if reference.no_back_populates and not reference.child.is_join_table:
                continue
            sub_object = SubObject(None, reference=reference, parent=self, parent_side=True)
            self.class_stmt.sub_objects[sub_object.code] = sub_object

    def get_sub_object(self, code):
        return self.class_stmt.sub_objects.get(code)

    def _init_unique_stmts(self):
        if self.table.is_join_table or not self.table.unique_keys:
            return
        unique_stmt = UniqueStmt('__table_args__', self, self.table.unique_keys)
        self.class_stmt.sub_objects['__table_args__'] = unique_stmt

    def _init_attributes(self):
        self.class_stmt.attributes['__tablename__'] = Variable('__tablename__', self, default=self.table.code)
        for code, column in self.table.columns.items():
            attribute = Attribute(column=column, parent=self)
            self.class_stmt.attributes[code] = attribute

    def _init_import_stmt(self):
        self.import_stmt.add_import('sqlalchemy', 'Column')
        if self.table.is_join_table:
            self.import_stmt.add_import('sqlalchemy', 'Table')

        for attribute in self.class_stmt.attributes.values():
            if isinstance(attribute, Attribute):
                self.import_stmt.add_import('sqlalchemy', attribute.type)
                if attribute.column.foreign_table:
                    self.import_stmt.add_import('sqlalchemy', 'ForeignKey')

        for sub_object in self.class_stmt.sub_objects.values():
            if isinstance(sub_object, UniqueStmt):
                self.import_stmt.add_import('sqlalchemy', 'UniqueConstraint')
            elif isinstance(sub_object, SubObject):
                self.import_stmt.add_import('sqlalchemy.orm', 'relationship')

        self.import_stmt.add_import(ctx_instance.base.package, ctx_instance.base.class_name)
