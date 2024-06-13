# -*- coding: utf-8 -*-
import os

from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.package import Package
from .schema_additional import SchemaAdditional


class SchemaAdditionalPackage(Package):
    def __init__(self):
        self.package = f'{ctx_instance.project_package}.schema'
        self.dir = os.path.join(ctx_instance.project_dir, 'schema')
        self.shcema_additionals = {}

        for code, schema in ctx_instance.schema_package.schemas.items():
            response_schemas = ctx_instance.response_schemas.get(code, {})
            create_schemas = ctx_instance.create_schemas.get(code, {})
            update_schemas = ctx_instance.update_schemas.get(code, {})
            if not response_schemas and not create_schemas and not update_schemas:
                continue
            additional_schema = SchemaAdditional(schema, response_schemas, create_schemas, update_schemas,
                                                 desc='schema_additional')
            self.shcema_additionals[code] = additional_schema

    def save(self):
        for schema_additional in self.shcema_additionals.values():
            schema_additional.save()
