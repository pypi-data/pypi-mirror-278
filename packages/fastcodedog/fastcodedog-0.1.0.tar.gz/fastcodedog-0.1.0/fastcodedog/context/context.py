# -*- coding: utf-8 -*-
from .base import Base
from .contextbase import ContextBase
from .modules import Modules
from .oauth2 import OAuth2
from .schema import Schema
from .tenant import Tenant


class Context(ContextBase):
    def __init__(self):
        super().__init__()
        self.pdm_files = []
        self.project_name = None
        self.author = None
        self.project_package = None
        self.project_dir = None
        # diagram的配置，这些配置也会在后续的生成代码中使用
        self.modules = Modules()
        self.tenant = Tenant()
        # model的配置
        self.base = Base()
        # schema的配置
        self.schema = Schema()
        self.response_schemas = {}
        self.create_schemas = {}
        self.update_schemas = {}
        # crud的配置
        self.queries = {}
        # api的配置
        self.extended_apps = {}
        self.oauth2 = OAuth2()
