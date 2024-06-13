# -*- coding: utf-8 -*-
import os

from fastcodedog.api.api import Api
from fastcodedog.api.config import Config
from fastcodedog.api.db import Db
from fastcodedog.api.main import Main
from fastcodedog.api.oauth import OAuth
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.package import Package
from fastcodedog.util.case_converter import camel_to_snake


class ApiPackage(Package):
    def __init__(self):
        self.package = f'{ctx_instance.project_package}.api'
        self.dir = os.path.join(ctx_instance.project_dir, 'api')

        self.config_dir = os.path.join(ctx_instance.project_dir, 'config')

        # 固定的文件
        self.config = Config(os.path.join(self.config_dir, 'config.py'), f'{ctx_instance.project_package}.config')
        self.db = Db(os.path.join(ctx_instance.project_dir, 'db.py'), f'{ctx_instance.project_package}.db')
        self.main = Main(os.path.join(ctx_instance.project_dir, 'main.py'), f'{ctx_instance.project_package}.main')
        self.oauth = OAuth(os.path.join(self.dir, 'oauth', 'oauth.py'),
                           f'{self.package}.oauth.oauth') if ctx_instance.oauth2.enabled else None
        # 计算属性
        self.apis = {}

        for code, crud in ctx_instance.crud_package.cruds.items():
            table = crud.schema.model.table
            path = os.path.join(self.dir, table.module, self.get_file_name(table))
            package = f'{self.package}.{table.module}.{camel_to_snake(self.get_class_name(table))}'
            api = Api(crud, path, package)
            self.apis[code] = api

        for api in self.apis.values():
            self.main.add_api(api)
        if self.oauth:
            self.main.add_api(self.oauth, as_='oauth_app')

    def save(self):
        self.config.save()
        self.db.save()
        for api in self.apis.values():
            api.save()
        self.main.save()
        if self.oauth:
            self.oauth.save()
