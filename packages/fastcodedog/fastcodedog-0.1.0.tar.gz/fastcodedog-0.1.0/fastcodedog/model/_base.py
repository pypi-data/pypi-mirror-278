# -*- coding: utf-8 -*-
from fastcodedog.generation.file import File


class _Base(File):
    def serialize(self):
        content = super().serialize()
        content += """from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
        return content
