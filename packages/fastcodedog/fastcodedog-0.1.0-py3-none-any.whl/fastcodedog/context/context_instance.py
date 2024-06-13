# -*- coding: utf-8 -*-
import json5

from fastcodedog.context.context import Context
from fastcodedog.util.deep_update import deep_update
from fastcodedog.util.find_file import find
from fastcodedog.util.singleton import Singleton


@Singleton
class ContextInstance(Context):
    def __init__(self):
        super().__init__()
        self.config_files = []
        self.diagram = None
        self.model_package = None
        self.schema_package = None
        self.schema_additional_package = None
        self.crud_package = None
        self.api_package = None

    def add_config(self, config_file):
        if config_file not in self.config_files:
            self.config_files.append(config_file)

    def add_pdm(self, pdm_file):
        if pdm_file not in self.context.pdm_files:
            self.context.pdm_files.append(pdm_file)

    def get_files(self, *args):
        files = []
        for arg in args:
            files.extend(find('.', arg))
        return list(dict.fromkeys(files))  # 保持顺序去重

    def load_config(self, *args):
        files = self.get_files(*args)
        for file in files:
            if file.endswith('.pdm'):
                self.add_pdm(file)
            if file.endswith('.json') or file.endswith('.json5'):
                self.add_config(file)

        config = {}
        for file in self.config_files:
            # 支持传入多个json文件，如果同一配置在多个文件中，则以排在最后的文件为准
            with open(file, 'r', encoding='utf-8') as f:
                config = deep_update(config, json5.load(f))
        return super().load(config)


ctx_instance = ContextInstance()
