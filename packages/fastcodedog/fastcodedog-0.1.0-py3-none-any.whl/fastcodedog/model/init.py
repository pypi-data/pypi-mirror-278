# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.file import File


class Init(File):
    def __init__(self, path, package, models, relation_objects):
        super().__init__(path, package)
        self.models = models
        self.relation_objects = relation_objects

        self._init_import_stmt()

    def _init_import_stmt(self):
        self.import_stmt.add_import(ctx_instance.base.package, ctx_instance.base.class_name)
        for model in self.models.values():
            self.import_stmt.add_import(model.package, model.class_name)
        for relation_object in self.relation_objects.values():
            self.import_stmt.add_import(relation_object.package, ', '.join(relation_object.variables.keys()))
