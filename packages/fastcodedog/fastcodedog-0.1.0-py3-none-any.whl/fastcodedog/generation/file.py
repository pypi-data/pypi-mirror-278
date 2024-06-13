# -*- coding: utf-8 -*-
import datetime
import os
from fastcodedog.generation.import_stmt import ImportStmt
from fastcodedog.util.indent import add_indent
from fastcodedog.util.write_file import write_python_file
from .generationbase import GenerationBase
from fastcodedog.context.context_instance import ctx_instance
from ..util.make_dirs import make_python_package_dirs


class File(GenerationBase):
    class AnnotationStmt:
        def __init__(self, path, desc, author=None, project_name=None, time=None):
            self.path = path
            self.desc = '本文件由自动生成脚本自动创建，请勿修改'
            if desc:
                self.desc += '\n' + desc
            self.author = author or ctx_instance.author
            self.project_name = project_name or ctx_instance.project_name
            self.file = os.path.split(path)[-1]
            self.time = time or self._get_create_time()

        def serialize(self, indent=''):
            return add_indent('"""\n' + \
                              f'@author: {self.author}\n' + \
                              f'@project: {self.project_name}\n' + \
                              f'@file: {self.file}\n' + \
                              f'@time: {self.time}\n' + \
                              f'@desc: {self.desc}\n' + \
                              '"""\n', indent)

        def _get_create_time(self):
            """
            从已经存在的文件里提取文件生成日期
            """
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as f:
                    keywords = '@time: '
                    old_file_content = f.read()
                    start = old_file_content.find(keywords)
                    if start == -1:
                        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    end = old_file_content.find('\n', start + 1)
                    if end == -1:
                        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return old_file_content[start + len(keywords):end]
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, path, package, desc=None):
        self.path = path
        self.package = package

        self.annotation_stmt = File.AnnotationStmt(path=self.path, desc=desc)
        self.import_stmt = ImportStmt()
        self.variables = {}
        self.function_blocks = {}
        self.class_blocks = {}

    def serialize(self):
        content = self.annotation_stmt.serialize()
        content += self.import_stmt.serialize()
        content += '\n'
        content += self.serialize_variable_stmt()
        content += self.serialize_function_blocks()
        content += self.serialize_class_blocks()
        return content

    def serialize_variable_stmt(self):
        content = ''
        for variable_stmt in self.variables.values():
            content += variable_stmt.serialize()
        return content

    def serialize_function_blocks(self):
        content = ''
        for function_block in self.function_blocks.values():
            content += function_block.serialize()
        return content

    def serialize_class_blocks(self):
        content = ''
        for classe_stmt in self.class_blocks.values():
            content += classe_stmt.serialize()
        return content

    def save(self):
        parent_dir = os.path.dirname(self.path)
        make_python_package_dirs(parent_dir, ctx_instance.project_dir)
        write_python_file(self.path, content=self.serialize())
