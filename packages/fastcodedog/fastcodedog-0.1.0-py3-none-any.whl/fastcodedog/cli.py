# -*- coding: utf-8 -*-
import sys

from fastcodedog.api.api_package import ApiPackage
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.crud.crud_package import CrudPackage
from fastcodedog.diagram.diagram import Diagram
from fastcodedog.model.model_package import ModelPackage
from fastcodedog.schema.schema_additional_package import SchemaAdditionalPackage
from fastcodedog.schema.schema_package import SchemaPackage


def main():
    if len(sys.argv) == 1:
        raise ValueError('缺少参数，请传入json5配置文件或者pdm文件')
    ctx_instance.load_config(*(sys.argv[1:]))
    ctx_instance.diagram = Diagram()
    ctx_instance.diagram.load()
    ctx_instance.model_package = ModelPackage()
    ctx_instance.model_package.save()
    ctx_instance.schema_package = SchemaPackage()
    ctx_instance.schema_package.save()
    ctx_instance.schema_additional_package = SchemaAdditionalPackage()
    ctx_instance.schema_additional_package.save()
    ctx_instance.crud_package = CrudPackage()
    ctx_instance.crud_package.save()
    ctx_instance.api_package = ApiPackage()
    ctx_instance.api_package.save()


if __name__ == '__main__':
    """    
$env:PYTHONPATH = "."
python fastcodedog/cli.py fastcodegen/test/fastframe.diagram.json5 fastcodegen/test/fastframe.model.json5
"""
    main()

