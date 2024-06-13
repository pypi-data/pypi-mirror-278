# -*- coding: utf-8 -*-
from .contextbase import ContextBase


class Modules(ContextBase):
    def __init__(self):
        super().__init__()
        self.specified_classe_names = {}
        self.writeable_modules = []
        self.readonly_modules = []
        self.force_foreignkeys = {}
        self.no_back_populates = []
