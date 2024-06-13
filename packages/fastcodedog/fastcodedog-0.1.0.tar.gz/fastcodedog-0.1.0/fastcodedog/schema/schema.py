# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.classs_block import ClassBlock
from fastcodedog.generation.file import File
from fastcodedog.generation.package import Package
from fastcodedog.generation.variable import Variable
from fastcodedog.model.attribute import Attribute as ModelAttribute
from .attribute import Attribute
from .schema_class_block import SchemaClassBlock
from ..generation.function_block import FunctionBlock
from ..util.case_converter import camel_to_snake, snake_to_camel


class Schema(File):
    def __init__(self, model, path, package, desc=None):
        super().__init__(path, package, desc=(desc or model.table.name))
        self.model = model
        self.code = model.code

        # 计算出的属性
        self.class_name = f'{Package.get_class_name(self.model.table)}'  # schema的基础类型，对应的create，update把版本在此基础上增加后缀
        self.dynamic_attributes_function = None
        # self.function_stmts
        # self.classe_stmts
        # self.import_stmt

        self._init_dynamic_attributes_functions(f'{self.class_name}Base')
        self._init_classes()
        self._init_import_stmt()

    def _init_classes(self):
        base_class_block = self.get_class_block('base', 'BaseModel')
        self.class_blocks[f'{base_class_block.name}'] = base_class_block
        base_class_name = base_class_block.name if not self.dynamic_attributes_function else f'{self.dynamic_attributes_function.name}()'
        for method in ['response', 'create', 'update']:
            class_block = self.get_class_block(method, base_class_name)
            self.class_blocks[f'{class_block.name}'] = class_block

    def get_class_block(self, method, base_class_name):
        class_name = f'{self.class_name}{snake_to_camel(method, upper_first=True)}' \
            if method != 'response' else self.class_name
        class_block = SchemaClassBlock(class_name, base_class_name, self, method)
        self.get_attributes(class_block)
        if method == 'base':
            class_block.config_class = self.get_confg_class_block(class_block)
        return class_block

    def get_attributes(self, parent_class_block):
        for m_attribute in self.model.class_stmt.attributes.values():
            if not isinstance(m_attribute, ModelAttribute):
                continue
            if (parent_class_block.method == 'base' and (m_attribute.code in ctx_instance.schema.no_response_attributes
                                                         or m_attribute.code in ctx_instance.schema.no_set_attributes or not m_attribute.column.nullable)):
                continue
            # 已经在base中，不需要再次添加
            if (
                    parent_class_block.method != 'base' and m_attribute.code not in ctx_instance.schema.no_response_attributes
                    and m_attribute.code not in ctx_instance.schema.no_set_attributes and m_attribute.column.nullable):
                continue
            if (parent_class_block.method == 'response' and
                    (m_attribute.code in ctx_instance.schema.no_response_attributes)):
                continue
            if (parent_class_block.method == 'create' and (m_attribute.code in ctx_instance.schema.no_set_attributes)):
                continue
            if (parent_class_block.method == 'update' and (m_attribute.code in ctx_instance.schema.no_set_attributes)):
                continue
            attribute = Attribute(m_attribute, parent_class_block)
            if parent_class_block.method == 'update':
                attribute.force_optional = True  # update的时候，允许不选非必填的参数
            parent_class_block.attributes[attribute.code] = attribute

    @staticmethod
    def get_confg_class_block(parent_class_block):
        config_class = ClassBlock('Config', None, parent_class_block)
        config_class.attributes['extra'] = Variable('extra', config_class, default='allow')
        config_class.attributes['orm_mode'] = Variable('orm_mode', config_class, default=True)
        config_class.attributes['allow_population_by_field_name'] = Variable('allow_population_by_field_name',
                                                                             config_class, default=True)
        if ctx_instance.schema.alias_generator.function:
            config_class.attributes['alias_generator'] = (
                Variable('alias_generator', config_class, type='function',
                         default=ctx_instance.schema.alias_generator.function))
        return config_class

    def _init_dynamic_attributes_functions(self, base_class_name):
        if ctx_instance.schema.dynamic_attributes_function.function:
            dynamic_class_name = f'Dynamic{base_class_name}'
            self.dynamic_attributes_function = FunctionBlock(f'get_dynamic_{camel_to_snake(base_class_name)}', self)
            self.dynamic_attributes_function.content = f"""dynamic_attributes = {ctx_instance.schema.dynamic_attributes_function.function}('{self.code}')
{dynamic_class_name} = type(
    '{dynamic_class_name}',
    ({base_class_name},),  # 这里根据实际需求调整基类
    {{
        '__annotations__': {{k: v[0] for k, v in dynamic_attributes.items()}},
        **{{k: v[1] for k, v in dynamic_attributes.items()}}
    }}
)
return {dynamic_class_name}
"""
            self.function_blocks[self.dynamic_attributes_function.name] = self.dynamic_attributes_function

    def _init_import_stmt(self):
        self.import_stmt.add_import('pydantic', 'BaseModel')
        self.import_stmt.add_import('pydantic', 'Field')
        self.import_stmt.add_import('typing', 'Optional')
        if ctx_instance.schema.alias_generator.import_stmt.get('import'):
            self.import_stmt.load_import(ctx_instance.schema.alias_generator.import_stmt)
        if ctx_instance.schema.dynamic_attributes_function.import_stmt.get('import'):
            self.import_stmt.load_import(ctx_instance.schema.dynamic_attributes_function.import_stmt)
        for class_block in self.class_blocks.values():
            for attibute in class_block.attributes.values():
                if attibute.type not in ['int', 'str', 'bool', 'float', 'bytes']:
                    self.import_stmt.add_import('pydantic', attibute.type)

    def get_schema_class_by_method(self, method):
        for class_block in self.class_blocks.values():
            if class_block.method == method:
                return class_block
        return None
