# -*- coding: utf-8 -*-
"""
@author: hubo
@project: fastframe
@file: class
@time: 2024/5/29 10:54
@desc:
"""

from .column import Column


class Table:
    """
    数据库表，父类负责数据模型
    """

    class ForeignReference:
        def __init__(self, parent_table, parent_column, child_table, child_column, no_back_populates=False):
            self.parent = parent_table  # Table或者Table的子类
            self.parent_column = parent_column
            self.child = child_table  # Table或者Table的子类
            self.child_column = child_column
            self.no_back_populates = no_back_populates

        def get_another_foreign_reference_of_child_table(self):
            """
            获取child_table的另一条外键关联，在child_table是join_table的时候有用
            :return:
            """
            if not self.child.is_join_table:  # 是否是关联表
                raise Exception(f'child_table {self.child.code} is not join_table')
            for child_reference in self.child.child_side_references:
                if child_reference.parent != self.parent:
                    return child_reference
            return None

    def __init__(self, node):
        self.node = node

        self.id = ''  # powerdesigner里的id
        self.module = ''  # 归属的module，对应pdm的diagram。根据table.code和module自动归属
        self.name = ''
        self.code = ''
        self.comment = ''
        self.columns = {}
        # # 主键，column.code列表，
        # self.primary_keys = {}  # {'key_1': [column1, column2, column3]}
        # 唯一约束，column.code列表
        self.unique_keys = {}  # {'key_2': [column4, column5, column6]}

        # 外键约束中被作为parent的部分
        self.parent_side_references = []  # [ForeignReference]
        # 外键约束中被作为child的部分
        self.child_side_references = []  # [ForeignReference]
        # 是否是关联表
        self.is_join_table = False

    def load(self):
        """
        从pdm中提取表的数据
        xml参考table.xml
        :return:
        """
        self.id = self.node.attrib.get('Id')
        self.name = self.node.find('{attribute}Name').text
        self.code = self.node.find('{attribute}Code').text
        if self.node.find('{attribute}Comment') is not None:
            self.comment = self.node.find('{attribute}Comment').text
        self.load_all_columns(self.node)
        # 继续找到主键和唯一键约束
        # 通过identity判断主键不准确，因为还有联合主键的情况
        self.get_all_keys()

    def set_join_table(self):
        # 判断是否是join_table
        self.is_join_table = (len(self.child_side_references) == len(self.columns))
        if self.is_join_table:
            # all_primary_columns = []
            # for keys in self.primary_keys.values():
            #     all_primary_columns += keys
            # all_primary_column_codes = [_.code for _ in all_primary_columns]
            for column in self.columns.values():
                if not column.primary_key:
                    raise Exception(
                        f'The table is join table, but the column is not primary key: {self.code}.{column.code}')

    def load_all_columns(self, node):
        """
        从pdm中提取表的列
        :param node:
        :return:
        """
        children = node.find('{collection}Columns')
        for child in children:
            if child.tag == '{object}Column' and child.attrib.get('Id') is not None:
                column = Column(self, child)
                column.load()
                self.columns[column.code] = column
                continue
            # self.get_all_columns(child)

    def get_all_keys(self):
        """
        从pdm中提取表的主键和唯一键
        :return:
        """
        children = self.node.find('{collection}Keys')
        for child in children:  # key节点
            if child.tag == '{object}Key' and child.attrib.get('Id') is not None:
                id = child.attrib.get('Id')
                code = child.find('{attribute}Code').text
                columns = []
                if child.find('{collection}Key.Columns'):
                    for column in child.find('{collection}Key.Columns').findall('{object}Column'):
                        columns.append(self.get_column_by_id(column.get('Ref')))
                    if self._is_primary_key(id):
                        # self.primary_keys[code] = columns
                        for column in columns:
                            column.primary_key = True
                    else:
                        self.unique_keys[code] = columns
                        if len(columns) == 1:
                            columns[0].unique = True

    def _is_primary_key(self, id):
        primary_key = self.node.find('{collection}PrimaryKey')
        if primary_key:
            primary_id = primary_key.find('{object}Key').get('Ref')
            if primary_id == id:
                return True
        return False

    def get_column_by_id(self, id):
        """
        通过id查找column，其中id是pdm里的id，<o:Column Id="o88">，<o:Column Ref="o88" />，o88是pdm里的id
        :param id:
        :return:
        """
        for column in self.columns.values():
            if column.id == id:
                return column

    def get_column_by_code(self, code):
        return self.columns.get(code)

    def add_parent_side_reference(self, reference):
        """
        添加外键中被作为parent的部分
        :param reference:
        :return:
        """
        self.parent_side_references.append(reference)

    def add_child_side_reference(self, reference):
        """
        添加外键中被作为child的部分
        :param reference:
        :return:
        """
        self.child_side_references.append(reference)
        reference.child_column.set_foreign_key(reference.parent, reference.parent_column)

    def get_primary_keys(self):
        primary_keys = []
        for column in self.columns.values():
            if column.primary_key:
                primary_keys.append(column.code)
        return primary_keys
