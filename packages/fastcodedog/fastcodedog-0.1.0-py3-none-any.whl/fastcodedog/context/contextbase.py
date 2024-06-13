# -*- coding: utf-8 -*-
class ContextBase:

    def load(self, json):
        for k, v in json.items():
            if hasattr(self, k) and isinstance(getattr(self, k), ContextBase):
                getattr(self, k).load(v)
            elif hasattr(self, k) and isinstance(getattr(self, k), dict):
                if not isinstance(v, dict):
                    raise Exception(f'{k} 需要是一个字典。 {self.__class__}')
                if (self.new_instance(k)):  # 字典中的value是一个对象
                    for kk, vv in v.items():
                        _v = self.new_instance(k)
                        _v.load(vv)
                        getattr(self, k).update({kk: _v})
                else:
                    getattr(self, k).update(v)
            elif hasattr(self, k) and isinstance(getattr(self, k), list):
                if not isinstance(v, list):
                    raise Exception(f'{k} 需要是一个列表。 {self.__class__}')
                _v = self.new_instance(k)
                if _v:
                    _v.load(v)
                    getattr(self, k).append(_v)
                else:
                    _v = getattr(self, k)
                    for vv in v:
                        if vv not in _v:
                            _v.append(vv)
            elif hasattr(self, k):
                setattr(self, k, v)
            else:
                raise Exception(f'{k} 不是一个有效的配置项。 {self.__class__}')

    @staticmethod
    def new_instance(config_name):
        return None
