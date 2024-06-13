# -*- coding: utf-8 -*-
from fastcodedog.generation.variable import Variable


class Param(Variable):
    def __init__(self, code, parent, type=None, schema_class_block=None, sub_object=None, nullable=True, default=None,
                 comment=None):
        super().__init__(code, parent, type, nullable, default, comment)
        self.schema_class_block = schema_class_block
        self.sub_object = sub_object

    def serialize(self):
        return super().serialize(force_serialize_type=True)
