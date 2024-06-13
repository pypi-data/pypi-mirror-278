"""
@author: fastcodedog
@project: fakeapp
@file: config.py
@time: 2024-06-12 15:34:22
@desc: 本文件由自动生成脚本自动创建，请勿修改
"""
import configparser
import os


def get_config(section=None, key=None, default=None):
    c_key = f'{section}.{key}'
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


_all_configs_ = {}
listion_port = get_config('app', 'port', 8000)
db_url = get_config('database', 'url', None)
