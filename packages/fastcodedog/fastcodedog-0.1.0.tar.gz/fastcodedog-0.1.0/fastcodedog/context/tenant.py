# -*- coding: utf-8 -*-
from .contextbase import ContextBase


class Tenant(ContextBase):
    def __init__(self):
        self.enabled = False
        self.tenant_table_code = None
        self.tenant_table_primary_key = None
        self.tenant_column = None
        self.no_tenant_column_tables = []
