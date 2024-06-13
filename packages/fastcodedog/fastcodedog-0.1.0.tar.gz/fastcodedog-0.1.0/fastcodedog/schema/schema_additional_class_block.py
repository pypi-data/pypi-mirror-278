# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.classs_block import ClassBlock
from fastcodedog.generation.variable import Variable
from fastcodedog.util.case_converter import snake_to_camel


class SchemaAdditionalClassBlock(ClassBlock):
    class SubObject(Variable):
        def __init__(self, code, class_nanme, schema_package, is_list, parent):
            super().__init__(code, parent)
            self.class_name = class_nanme
            self.schema_package = schema_package
            self.is_list = is_list

        def serialize(self):
            content = f"{self.code}: "
            if self.is_list:
                content += f"List[{self.class_name}] = []"
            else:
                content += f"{self.class_name} = None"
            return content + '\n'

    def __init__(self, name, schema, method, additional_schema_element_expressions, parent):
        base_class = schema.class_name if method == 'response' else f'{schema.class_name}{snake_to_camel(method, upper_first=True)}'
        super().__init__(name, base_class, parent)
        self.schema = schema
        self.method = method
        self.additional_schema_element_expressions = additional_schema_element_expressions
        self.model = self.schema.model

        # 需要计算的竖向
        # sub_objects
        # self.sub_classes

        self._init_sub_objects()

    def _init_sub_objects(self):
        for expression in self.additional_schema_element_expressions:
            sub_object_name, sub_object_elements = self.parse_element_expression(expression)
            sub_object_class_name, sub_object_schema, is_list = self.create_or_get_sub_class(sub_object_elements,
                                                                                             self.model)
            if sub_object_class_name:
                self.sub_objects[sub_object_name] = SchemaAdditionalClassBlock.SubObject(sub_object_name,
                                                                                         sub_object_class_name,
                                                                                         sub_object_schema.package if sub_object_schema else None,
                                                                                         is_list, self)

    def create_sub_classes(self):
        for sub_object_name, sub_object in self.sub_objects.items():
            self.sub_classes[sub_object_name] = sub_object

    def create_or_get_sub_class(self, sub_object_elements, model):
        cur_element = sub_object_elements[0]
        cur_sub_object_in_model = model.get_sub_object(cur_element)
        if not cur_sub_object_in_model:
            raise Exception(f'{self.schema.code}的附加schema的配置有误，{cur_element}不存在')
        next_model = ctx_instance.model_package.models.get(cur_sub_object_in_model.back_populate_table.code)
        next_schema = ctx_instance.schema_package.schemas.get(cur_sub_object_in_model.back_populate_table.code)
        is_list = cur_sub_object_in_model.is_list
        next_class_name = next_schema.class_name if self.method == 'response' \
            else f'{next_schema.class_name}{snake_to_camel(self.method, upper_first=True)}'
        if len(sub_object_elements) == 1:
            return next_class_name, next_schema, is_list

        next_class_name = '_' + next_class_name
        next_sub_object_express = '.'.join(sub_object_elements[1:])
        sub_class = SchemaAdditionalClassBlock(next_class_name, next_schema, self.method, [next_sub_object_express],
                                               self)
        self.sub_classes[next_class_name] = sub_class
        return next_class_name, None, is_list

    def parse_element_expression(self, element_expression):
        # 把附加schema的属性表达式解析成两部分，第一部分是附加schema的属性名字，第二部分是附加schema的属性包含的元素列表
        if isinstance(element_expression, dict):
            # 第一个种格式，直接就是字典 sub_object_name：additional_sub_object_elements
            # {user_menus: "positions.menus"}
            elements = list(element_expression.values())[0]
            if elements.find('#') >= 0:
                raise Exception(f'{self.name}的附加schema的配置有误，字典性配置中{elements}不能包含#号')
            return list(element_expression.keys())[0], elements.split('.')
        if element_expression.find('#') >= 0:
            # 用#指定变量名
            # positions.menus#menus
            if element_expression.count('#') != 1:
                raise Exception(f'{self.name}的附加schema的配置有误，{element_expression}只能包含一个#号')
            return element_expression[element_expression.find('#') + 1:], element_expression[
                                                                          :element_expression.find('#')].split('.')
        if element_expression.find('.') >= 0:
            # 没有指定变量名，使用默认的变量名
            return element_expression[:element_expression.find('.')], element_expression.split('.')
        return element_expression, [element_expression]
