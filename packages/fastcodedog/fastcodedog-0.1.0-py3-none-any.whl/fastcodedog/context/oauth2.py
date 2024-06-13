# -*- coding: utf-8 -*-
from .contextbase import ContextBase


class OAuth2(ContextBase):
    def __init__(self):
        super().__init__()
        self.enabled = False
        self.user_table = None
        self.user_name_field = None
        self.user_password_field = None
