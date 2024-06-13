# -*- coding: utf-8 -*-
"""
@author: hubo
@project: fastframe
@file: attribute
@time: 2024/5/29 10:55
@desc:
"""


class Column:
    """
    列，父类负责数据模型
    """

    def __init__(self, table, node):
        self.table = table
        self.node = node

        self.id = ''  # powerdesigner里的id
        self.name = ''
        self.code = ''
        self.comment = ''
        self.data_type = ''
        self.length = None
        self.nullable = True
        self.identity = False  # 生成：sqlalchemyIdentity(start=42, cycle=True)等之类

        # 需要从全局查找并填充
        self.primary_key = False
        self.unique = False
        self.foreign_table = None  # 外键对应的表
        self.foreign_column = None  # 外键对应的列

    def load(self):
        """
        从pdm中提取列的数据
        xml参考table.xml中<c:Columns>的部分
        :return:
        """
        self.id = self.node.attrib.get('Id')
        for child in self.node:
            if child.tag == '{attribute}Name':
                self.name = child.text
            if child.tag == '{attribute}Code':
                self.code = child.text
            if child.tag == '{attribute}Comment':
                self.comment = child.text
            if child.tag == '{attribute}DataType':
                self.data_type = child.text
            if child.tag == '{attribute}Length':
                self.length = int(child.text)
            if child.tag == '{attribute}Column.Mandatory' and child.text == '1':
                self.nullable = False

    def set_foreign_key(self, foreign_table, foreign_column):
        """
        设置外键.
        :param foreign_table:
        :param foreign_column:
        :return:
        """
        self.foreign_table = foreign_table
        self.foreign_column = foreign_column
