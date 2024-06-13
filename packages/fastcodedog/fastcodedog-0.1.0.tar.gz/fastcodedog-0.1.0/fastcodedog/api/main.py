# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.generation.file import File
from fastcodedog.generation.variable import Variable
from fastcodedog.util.case_converter import camel_to_snake


class Main(File):
    def __init__(self, path, package, desc=None):
        super().__init__(path, package, desc)

        self.script_lines = []
        self.main_content = """if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8000)
        """
        self._init_import_stmt()
        self._init_variables()
        self._init_script_lines()
        self._init_extended_apps()

    def _init_extended_apps(self):
        for api_name, api_package in ctx_instance.extended_apps.items():
            self.import_stmt.add_import(api_package, 'app', f'{api_name}_app')
            self.script_lines.append(f'app.include_router({api_name}_app.router)')

    def _init_script_lines(self):
        self.script_lines.extend("""@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database operation failed: {exc}",
    )
""".splitlines())
        self.script_lines.append('logging.basicConfig()')
        self.script_lines.append("logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)")

    def _init_variables(self):
        self.variables['app'] = Variable('app', self, default='FastAPI()')

    def _init_import_stmt(self):
        self.import_stmt.add_import(None, 'uvicorn')
        self.import_stmt.add_import(None, 'logging')
        self.import_stmt.add_import('fastapi', 'FastAPI')
        self.import_stmt.add_import('fastapi', 'HTTPException')
        self.import_stmt.add_import('sqlalchemy.exc', 'SQLAlchemyError')
        self.import_stmt.add_import('starlette.status', 'HTTP_500_INTERNAL_SERVER_ERROR')

    def add_api(self, api, as_=None):
        if not as_:
            as_ = f'{camel_to_snake(api.model.class_name)}_app'
        self.import_stmt.add_import(api.package, 'app', as_)
        self.script_lines.append(f'app.include_router({as_}.router)')

    def serialize(self):
        content = super().serialize()
        for line in self.script_lines:
            content += line + '\n'
        content += '\n'
        content += self.main_content
        return content
