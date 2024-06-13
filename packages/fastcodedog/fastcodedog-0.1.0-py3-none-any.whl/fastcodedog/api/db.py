# -*- coding: utf-8 -*-
from fastcodedog.generation.file import File
from fastcodedog.generation.function_block import FunctionBlock
from fastcodedog.generation.variable import Variable


class Db(File):
    def __init__(self, path, package, desc=None):
        super().__init__(path, package, desc)
        self._init_import_stmt()
        self._init_funciton()
        self._init_variables()

    def _init_import_stmt(self):
        self.import_stmt.add_import('sqlalchemy', 'create_engine')
        self.import_stmt.add_import('sqlalchemy.orm', 'sessionmaker')
        self.import_stmt.add_import('.config.config', 'db_url')

    def _init_variables(self):
        self.variables['engine'] = Variable('engine', self, type='function', default="create_engine(db_url)")
        self.variables['Session'] = Variable('Session', self, type='function', default="sessionmaker(bind=engine)")

    def _init_funciton(self):
        func = FunctionBlock('get_session', self)
        func.content = f"""session = Session()
try:
    yield session
finally:
    session.close()
        """
        self.function_blocks[func.name] = func
