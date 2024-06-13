# -*- coding: utf-8 -*-
from fastcodedog.generation.package import Package
from fastcodedog.generation.variable import Variable
from fastcodedog.util.case_converter import camel_to_snake
from fastcodedog.util.inflect_wrapper import plural


class SubObject(Variable):
    def __init__(self, code, parent, reference, parent_side):
        super().__init__(code, parent)
        self.reference = reference
        self.parent_side = parent_side

        # 计算出的属性
        # self.code
        self.no_back_populates = False  # 不生成反向映射
        self.table = None
        self.back_populates = None
        self.back_populate_table = None
        self.back_populate_class_name = None
        self.foreign_keys = None  # 实际只有一个，同一个表之间的关联，需要指定foreign_keys
        self.secondary = None  # 多对多关联
        self.remote_side = None  # 同一个表指向自己的时候，需要指定remote_side
        self.is_list = False
        self.refer_to_join_table = False  # 是否连接到join_table
        self.cascade = None

        self._init()

    def _init(self):
        if self.reference.child.is_join_table:
            # 找到self.reference.child_table中的另一个字段
            another_reference = self.reference.get_another_foreign_reference_of_child_table()
            if not another_reference:
                raise Exception(f'在关联表{self.reference.child.code}中找不到另一条的外键关联')
            self.code = another_reference.child_column.code
            self.back_populate_table = another_reference.parent
            self.back_populates = self.reference.child_column.code
            self.table = self.reference.parent
            if self.back_populates.endswith('_id'):
                self.back_populates = self.back_populates[:-3]
            self.back_populates = plural(self.back_populates)
            if self.code.endswith('_id'):
                self.code = self.code[:-3]
            self.code = plural(self.code)
            # 填充更多值
            self.refer_to_join_table = True
            self.back_populate_class_name = Package.get_class_name(self.back_populate_table)
            self.secondary = self.reference.child.code
            self.is_list = True
        else:
            child_object_name = self.reference.child_column.code
            child = self.reference.child
            parent_object_name = plural(camel_to_snake(Package.get_class_name(self.reference.child)))
            parent = self.reference.parent
            # 一些特殊命名规则
            if self.reference.child_column.code in ['parent', 'parent_id']:
                parent_object_name = 'children'
            if child_object_name.endswith('_id'):
                child_object_name = child_object_name[:-3]
            if self.parent_side:
                self.code = parent_object_name
                self.table = parent
                self.back_populates = child_object_name
                self.back_populate_table = child
                # 更多变量
                self.back_populate_class_name = Package.get_class_name(self.back_populate_table)
                if self.reference.parent.code == self.reference.child.code:
                    self.foreign_keys = self.reference.child_column.code
                    self.remote_side = self.reference.child_column.code
                self.cascade = 'save-update, merge, delete'
                self.is_list = True
            else:
                self.code = child_object_name
                self.table = child
                self.back_populates = parent_object_name
                self.back_populate_table = parent
                # 更多变量
                self.back_populate_class_name = Package.get_class_name(self.back_populate_table)
                self.foreign_keys = self.reference.child_column.code
                if self.reference.parent.code == self.reference.child.code:
                    self.remote_side = self.reference.parent_column.code
                self.no_back_populates = self.reference.no_back_populates
                self.is_list = False

    def serialize(self):
        content = f"{self.code} = relationship('{self.back_populate_class_name}'"
        if self.foreign_keys:
            content += f", foreign_keys={self.foreign_keys}"
        if self.remote_side:
            content += f", remote_side={self.remote_side}"
        if self.secondary:
            content += f", secondary='{self.secondary}'"
        if self.cascade:
            content += f", cascade='{self.cascade}'"
        if self.no_back_populates:
            content += ')  # no_back_populates'
        else:
            content += f", back_populates='{self.back_populates}')"
        return content + '\n'
