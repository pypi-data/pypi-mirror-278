# -*- coding: utf-8 -*-
class Query:
    """
    还没有归并到context体系里面，因此还需要周董设置
    """

    class Parameter:
        def __init__(self, json):
            self.nullable = True
            self.description = None
            self.default = None
            if isinstance(json, dict):
                self.type = json.get('type')
                self.nullable = json.get('nullable', True)
                self.description = json.get('description')
                self.default = json.get('default')
            else:
                self.type = json

    def __init__(self, json):
        self.parameters = {k: Query.Parameter(v) for k, v in json.get('parameters', {}).items()}
        self.filters = json.get('filters', [])
        self.aliases = {k: v for k, v in json.get('aliases', {}).items()}
        self.joins = json.get('joins', [])
        self.outerjoins = json.get('outerjoins', [])
