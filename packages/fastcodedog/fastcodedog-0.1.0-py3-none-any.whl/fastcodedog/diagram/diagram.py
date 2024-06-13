# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

from fastcodedog.context.context_instance import ctx_instance
from .column import Column
from .table import Table


class Diagram:
    def __init__(self):
        self.tables = {}

    def load(self):
        if not ctx_instance.pdm_files:
            raise Exception('没有需要处理的pdm文件')
        # 装载所有表
        for pdm_file in ctx_instance.pdm_files:
            tree = ET.parse(pdm_file)
            root = tree.getroot()
            self._load_all_tables(root)


        # 装载所有表之间的关联外键关联
        for pdm_file in ctx_instance.pdm_files:
            tree = ET.parse(pdm_file)
            root = tree.getroot()
            # 填充外键
            self.fill_foreign_keys(root)

        # 判断是否是join表
        for table in self.tables.values():
            table.set_join_table()

        # 增加tenant
        if ctx_instance.tenant.enabled:
            self._check_or_create_tenant_table()
            self.add_tenant_column_to_all_tables()  # 会同步修改所有的unique
            self.add_tenant_foreign_key_context()

        # 增加强制的外键。放最后，因为tenant可能是程序生成的，并且可能所有表都有外键指向tenant
        self.fill_force_foreign_references()

    def add_tenant_foreign_key_context(self):
        ctx_instance.modules.force_foreignkeys[f'{ctx_instance.tenant.tenant_table_code}.{ctx_instance.tenant.tenant_table_primary_key}'] = [ctx_instance.tenant.tenant_column]
        ctx_instance.modules.no_back_populates.append(ctx_instance.tenant.tenant_column)
        ctx_instance.schema.no_response_attributes.append(ctx_instance.tenant.tenant_column)
        ctx_instance.schema.no_set_attributes.append(ctx_instance.tenant.tenant_column)

    def fill_force_foreign_references(self):
        for parent_key, child_keys in ctx_instance.modules.force_foreignkeys.items():
            parent_table_code = parent_key.split('.')[0]
            parent_table = self.tables.get(parent_table_code)
            parent_column_code = parent_table.get_column_by_code(parent_key.split('.')[1])
            parent_column = parent_table.get_column_by_code(parent_column_code.code)
            for child_key in child_keys:
                child_table_code = None if child_key.find('.') == -1 else child_key.split('.')[0]
                child_column_code = child_key if child_key.find('.') == -1 else child_key.split('.')[1]
                for child_table in self.tables.values():
                    # 表是否匹配
                    if parent_table.code == child_table.code:
                        continue
                    if child_table_code and child_table_code != child_table.code:
                        continue
                    # 字段是否匹配
                    child_column = child_table.get_column_by_code(child_column_code)
                    if not child_column:
                        continue
                    if child_column.foreign_table:
                        continue
                    reference = Table.ForeignReference(parent_table, parent_column, child_table, child_column)
                    if (child_column.code in ctx_instance.modules.no_back_populates
                            or f'{child_table.code}.{child_column.code}' in ctx_instance.modules.no_back_populates):
                        # 目前默认强制管理都不需要反向映射的情况，比如tenant_id如果反向映射，则数据量太大了
                        # 将来遇到需要反向映射的时候再说
                        reference.no_back_populates = True
                    parent_table.add_parent_side_reference(reference)
                    child_table.add_child_side_reference(reference)

    def fill_foreign_keys(self, node):
        """
        填充外键.xml参考reference.xml
        :param node:
        :return:
        """
        for child in node:
            if child.tag == '{object}Reference' and child.find('{collection}ParentTable'):
                # parent_table
                parent_table_id = child.find('{collection}ParentTable').find('{object}Table').get('Ref')
                # child_table
                child_table_id = child.find('{collection}ChildTable').find('{object}Table').get('Ref')
                # parent_table.column
                parent_column_id = child.find('{collection}Joins').find('{object}ReferenceJoin').find(
                    '{collection}Object1').find('{object}Column').get('Ref')
                # child_table.column
                child_column_id = child.find('{collection}Joins').find('{object}ReferenceJoin').find(
                    '{collection}Object2').find('{object}Column').get('Ref')
                # 回填
                parent_table = self.get_table_by_id(parent_table_id)
                child_table = self.get_table_by_id(child_table_id)
                if not parent_table or not child_table:
                    continue
                parent_column = parent_table.get_column_by_id(parent_column_id)
                child_column = child_table.get_column_by_id(child_column_id)
                child_column.foreign_table = parent_table
                child_column.foreign_column = parent_column
                child_key = f'{child_table.code}.{child_column.code}'
                reference = Table.ForeignReference(parent_table, parent_column, child_table, child_column)
                if (child_column.code in ctx_instance.modules.no_back_populates
                        or child_key in ctx_instance.modules.no_back_populates):
                    # 不需要反向映射的情况，比如tenant_id如果反向映射，则数据量太大了
                    reference.no_back_populates = True
                parent_table.add_parent_side_reference(reference)
                child_table.add_child_side_reference(reference)
                continue
            self.fill_foreign_keys(child)

    def _check_or_create_tenant_table(self):
        tenant_table = self.tables.get(ctx_instance.tenant.tenant_table_code)
        if not tenant_table:
            tenant_table = Table(None)
            tenant_table.code = ctx_instance.tenant.tenant_table_code
            tenant_table.name = '租户'
            tenant_table.module = self._get_table_module(tenant_table.code)
            self.tables[tenant_table.code] = tenant_table
        # 确保domain存在
        for k, v in {ctx_instance.tenant.tenant_table_primary_key: ('int', 11),
                     'domain': ('varchar', 64), 'name': ('varchar', 255), 'enabled': ('boolean', 1)}.items():
            if k not in tenant_table.columns:
                column = Column(tenant_table, None)
                column.id = k
                column.code = k
                column.data_type = v[0]
                column.length = v[1]
                column.nullable = False
                tenant_table.columns[k] = column
        # tenant_table.primary_keys[f'key_tenant_{ctx_instance.tenant.tenant_table_primary_key}'] =\
        #     [tenant_table.columns[ctx_instance.tenant.tenant_table_primary_key]]
        tenant_table.columns[ctx_instance.tenant.tenant_table_primary_key].primary_key = True
        tenant_table.unique_keys['key_tenant_domain'] = [tenant_table.columns['domain']]

    def add_tenant_column_to_all_tables(self):
        for table in self.tables.values():
            if table.is_join_table or table.code == ctx_instance.tenant.tenant_table_code \
                    or table.code in ctx_instance.tenant.no_tenant_column_tables:
                continue
            table.columns[ctx_instance.tenant.tenant_column] = Column(table, None)
            table.columns[ctx_instance.tenant.tenant_column].name = '租户'
            table.columns[ctx_instance.tenant.tenant_column].code = ctx_instance.tenant.tenant_column
            table.columns[ctx_instance.tenant.tenant_column].data_type = 'int'
            table.columns[ctx_instance.tenant.tenant_column].length = '11'
            table.columns[ctx_instance.tenant.tenant_column].nullable = False
            # 每个unique都加上对应字段
            for unique_key_columns in table.unique_keys.values():
                for column in unique_key_columns:
                    column.unique = False   # 所有的unique都变成和tenant_id的联合unique
                unique_key_columns.append(table.columns[ctx_instance.tenant.tenant_column])

    def _load_all_tables(self, node):
        for child in node:
            if child.tag == '{object}Table' and child.attrib.get('Id') is not None:
                table = Table(child)
                table.load()
                module = self._get_table_module(table.code)
                if not module:
                    continue
                table.module = module
                self.tables[table.code] = table
                continue
            self._load_all_tables(child)

    @staticmethod
    def _get_table_module(table_code):
        for module in ctx_instance.modules.writeable_modules + ctx_instance.modules.readonly_modules:
            if table_code.startswith(module):
                return module
        return None

    def get_table_by_id(self, id):
        """
        根据pdm文件中的id获取表
        id通常是如下两个形式<o:Table Ref="o29"/>，<o:Table Id="o29">其中o29是表的id
        :param id:
        :return:
        """
        for t in self.tables.values():
            if t.id == id:
                return t
        return None
