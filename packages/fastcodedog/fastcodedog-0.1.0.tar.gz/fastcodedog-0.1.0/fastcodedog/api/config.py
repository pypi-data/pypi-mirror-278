# -*- coding: utf-8 -*-

from fastcodedog.generation.file import File
from fastcodedog.generation.function_block import FunctionBlock
from fastcodedog.generation.variable import Variable


class Config(File):
    def __init__(self, path, package, desc=None):
        super().__init__(path, package, desc)
        self.config_file = path[:-3] + '.ini'
        self.config_content = self._get_config_content()
        self._init_import_stmt()
        self._init_funciton()
        self._init_variables()

    def _init_variables(self):
        self.variables['_all_configs_'] = Variable('_all_configs_', self, type=dict, default={})
        self.variables['listion_port'] = Variable('listion_port', self, type='function',
                                                  default="get_config('app', 'port', 8000)")
        self.variables['db_url'] = Variable('db_url', self, type='function',
                                            default="get_config('database', 'url', None)")

    def _init_funciton(self):
        func = FunctionBlock('get_config', self)
        func.params['section'] = Variable('section', func)
        func.params['key'] = Variable('key', func)
        func.params['default'] = Variable('default', func, default=None)
        func.content = f"""c_key = f'{{section}}.{{key}}'
if c_key not in _all_configs_:
    confif_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    config.read(confif_file)
    _all_configs_[c_key] = None
    if section in config and config.get(section, key):
        _all_configs_[c_key] = config.get(section, key)
if c_key in _all_configs_ and _all_configs_[c_key] is not None:
    return _all_configs_[c_key]
return default
"""
        self.function_blocks['get_config'] = func

    def _init_import_stmt(self):
        self.import_stmt.add_import(from_=None, import_='configparser')
        self.import_stmt.add_import(from_=None, import_='os')

    def _get_config_content(self):
        return """[app]
port=8000

[database]
url=postgresql://ccuser:Cc_12345678@192.168.44.128:15432/ccdb
"""

    def serialize(self):
        content = self.annotation_stmt.serialize()
        content += self.import_stmt.serialize()
        content += '\n'
        content += self.serialize_function_blocks()
        content += self.serialize_variable_stmt()
        content += self.serialize_class_blocks()
        return content

    def save(self):
        super().save()
        # 写一份配置文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(self.config_content)
