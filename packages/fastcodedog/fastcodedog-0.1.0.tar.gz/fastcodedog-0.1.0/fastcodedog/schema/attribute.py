# -*- coding: utf-8 -*-
from fastcodedog.generation.variable import Variable
from fastcodedog.util.type_converter import database_type_to_pydantic_type


class Attribute(Variable):
    def __init__(self, model_attribute, parent, comment=None, force_optional=False):
        super().__init__(model_attribute.code, parent, model_attribute.type,
                         comment=comment or model_attribute.column.name)
        self.model_attribute = model_attribute
        self.code = model_attribute.code
        self.force_optional = force_optional
        self.nullable = self.model_attribute.column.nullable

        # 需要计算的属性
        self.type_with_length = None

        self.type, self.type_with_length = database_type_to_pydantic_type(self.model_attribute.column.data_type,
                                                                          self.model_attribute.column.length)

    def serialize(self):
        type_str = self.type_with_length
        if self.model_attribute.column.nullable or self.force_optional:
            type_str = f'Optional[{type_str}]'
        field_params = ['None']
        if self.comment and self.comment != '':
            field_params.append(f'description="{self.comment}"')
        field_str = f'Field({", ".join(field_params)})'
        return f'{self.code}: {type_str} = {field_str}\n'
