# -*- coding: utf-8 -*-
from .contextbase import ContextBase


class Base(ContextBase):
    def __init__(self):
        super().__init__()
        self.class_name = None
        self.package = None
