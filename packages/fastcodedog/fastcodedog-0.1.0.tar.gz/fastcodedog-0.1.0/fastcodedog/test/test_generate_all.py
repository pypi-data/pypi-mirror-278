# -*- coding: utf-8 -*-
from fastcodedog.api.api_package import ApiPackage
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.crud.crud_package import CrudPackage
from fastcodedog.diagram.diagram import Diagram
from fastcodedog.model.model_package import ModelPackage
from fastcodedog.schema.schema_additional_package import SchemaAdditionalPackage
from fastcodedog.schema.schema_package import SchemaPackage


def test_diagram():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ...


def test_model():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ctx_instance.model_package = ModelPackage()
    ctx_instance.model_package.save()


def test_schema():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ctx_instance.model_package = ModelPackage()
    ctx_instance.schema_package = SchemaPackage()
    ctx_instance.schema_additional_package = SchemaAdditionalPackage()
    ctx_instance.schema_package.save()
    ctx_instance.schema_additional_package.save()


def test_crud():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ctx_instance.model_package = ModelPackage()
    ctx_instance.schema_package = SchemaPackage()
    ctx_instance.schema_additional_package = SchemaAdditionalPackage()
    ctx_instance.crud_package = CrudPackage()
    ctx_instance.crud_package.save()


def test_api():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ctx_instance.model_package = ModelPackage()
    ctx_instance.schema_package = SchemaPackage()
    ctx_instance.schema_additional_package = SchemaAdditionalPackage()
    ctx_instance.crud_package = CrudPackage()
    ctx_instance.api_package = ApiPackage()
    ctx_instance.api_package.save()
