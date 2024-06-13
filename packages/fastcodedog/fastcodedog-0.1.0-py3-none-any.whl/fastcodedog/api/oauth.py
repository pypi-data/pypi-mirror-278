# -*- coding: utf-8 -*-
from fastcodedog.api.app_function import AppFunction
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.crud.param import Param
from fastcodedog.generation.file import File
from fastcodedog.generation.variable import Variable


def enable_api_oauth2(cls):
    if ctx_instance.oauth2.enabled:
        cls.import_stmt.add_import('fastapi.security', 'OAuth2PasswordBearer')
        cls.import_stmt.add_import('typing', 'Annotated')
        cls.variables['oauth2_scheme '] = Variable('oauth2_scheme ', cls,
                                                   default="OAuth2PasswordBearer(tokenUrl='/oauth/token')")
        cls.extra_function_params['token'] = Param('token', parent=cls, type='Annotated[str, Depends(oauth2_scheme)]',
                                                   nullable=False)
        cls.extra_function_params_when_get['token'] = Param('token', parent=cls,
                                                            type='Annotated[str, Depends(oauth2_scheme)]',
                                                            nullable=False)
        cls.extra_function_params_when_get_list['token'] = Param('token', parent=cls,
                                                                 type='Annotated[str, Depends(oauth2_scheme)]',
                                                                 nullable=False)


class OAuth(File):
    def __init__(self, path, package, desc=None):
        desc = """
OAuth2.SECRET_KEY =
OAuth2.EXPIRE_SECONDS = 60*60*2
OAuth2.REDIS_URL = 'redis://localhost:6379/oauth2'
"""
        super().__init__(path, package, desc)

        self.user_model = ctx_instance.model_package.models.get(ctx_instance.oauth2.user_table)
        self.tenant_model = ctx_instance.model_package.models.get(
            ctx_instance.tenant.tenant_table_code) if ctx_instance.tenant.enabled else None
        self.param_session = Param('session', parent=self, type='Session', default='Depends(get_session)')
        self.param_token = Param('token', parent=self, type='Annotated[str, Depends(oauth2_scheme)]', nullable=False)
        self._init_import_stmt()
        self._init_variables()
        self._init_functions()

    def _init_functions(self):
        self._init_login_function()
        self._init_remove_token_function()
        self._init_refresh_token_function()
        self._init_read_user_me_function()

    def _init_read_user_me_function(self):
        app_func = AppFunction('read_users_me', self, 'get', '/oauth/me')
        app_func.params['token'] = self.param_token
        app_func.content = 'return OAuth2.get_token_user(token)\n'
        self.function_blocks[app_func.name] = app_func

    def _init_refresh_token_function(self):
        app_func = AppFunction('refresh_token', self, 'post', '/oauth/refresh_token', reponse_model='Token')
        app_func.params['token'] = self.param_token
        app_func.content = 'return OAuth2.refresh_token(token)\n'
        self.function_blocks[app_func.name] = app_func

    def _init_remove_token_function(self):
        app_func = AppFunction('remove_token', self, 'post', '/oauth/logout')
        app_func.params['token'] = self.param_token
        app_func.content = 'OAuth2.remove_token(token)\n'
        app_func.content += 'return {}\n'
        self.function_blocks[app_func.name] = app_func

    def _init_login_function(self):
        app_func = AppFunction('login_for_access_token', self, 'post', '/oauth/token', reponse_model='Token')
        app_func.params['form_data'] = Param('form_data', parent=self,
                                             type='Annotated[OAuth2PasswordRequestForm, Depends()]', nullable=False)
        app_func.params['session'] = self.param_session
        app_func.content = 'username = form_data.username\n'
        app_func.content += 'password = form_data.password\n'
        if ctx_instance.tenant.enabled:
            app_func.content += "if username.find('@') == -1:\n"
            app_func.content += '    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username. Must contain \'@\'")\n'
            app_func.content += 'domain = username.split(\'@\')[1]\n'
            app_func.content += 'username = username.split(\'@\')[0]\n'
            app_func.content += (f'user = session.query({self.user_model.class_name})'
                                 f'.join({self.tenant_model.class_name}, {self.user_model.class_name}.{ctx_instance.tenant.tenant_column}=={self.tenant_model.class_name}.id)'
                                 f'.filter({self.user_model.class_name}.{ctx_instance.oauth2.user_name_field}==username)'
                                 f'.filter({self.user_model.class_name}.{ctx_instance.oauth2.user_password_field}==password)'
                                 f'.filter({self.tenant_model.class_name}.domain==domain)'
                                 f'.first()\n')
        else:
            app_func.content += (f'user = session.query({self.user_model.class_name})'
                                 f'.filter({self.user_model.class_name}.{ctx_instance.oauth2.user_name_field}==username)'
                                 f'.filter({self.user_model.class_name}.{ctx_instance.oauth2.user_password_field}==password)'
                                 f'.first()\n')
        app_func.content += 'if user:\n'
        token_content = ', '.join([f'"{k}": user.{k}' for k in self.user_model.table.get_primary_keys()])
        token_content += f', "{ctx_instance.oauth2.user_name_field}": username'
        if ctx_instance.tenant.enabled:
            token_content += f', "{ctx_instance.tenant.tenant_column}": user.{ctx_instance.tenant.tenant_column}'
        token_content = '{' + token_content + '}'
        app_func.content += f'    return OAuth2.create_access_token({token_content})\n'
        app_func.content += 'raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")\n'
        self.function_blocks[app_func.name] = app_func

    def _init_variables(self):
        self.variables['app'] = Variable('app', self, default="FastAPI()")
        self.variables['oauth2_scheme '] = Variable('oauth2_scheme ', self,
                                                    default="OAuth2PasswordBearer(tokenUrl='/oauth/token')")

    def _init_import_stmt(self):
        self.import_stmt.add_import('typing', 'Annotated')
        self.import_stmt.add_import('fastoauth', 'OAuth2')
        self.import_stmt.add_import('fastoauth', 'Token')
        self.import_stmt.add_import('fastapi', 'Depends')
        self.import_stmt.add_import('fastapi', 'FastAPI')
        self.import_stmt.add_import('fastapi', 'HTTPException')
        self.import_stmt.add_import('fastapi', 'status')
        self.import_stmt.add_import('fastapi.security', 'OAuth2PasswordBearer')
        self.import_stmt.add_import('fastapi.security', 'OAuth2PasswordRequestForm')
        self.import_stmt.add_import(f'{ctx_instance.project_package}.db', 'Session')
        self.import_stmt.add_import(f'{ctx_instance.project_package}.db', 'get_session')
        self.import_stmt.add_import(self.user_model.package, self.user_model.class_name)
        if self.tenant_model:
            self.import_stmt.add_import(self.tenant_model.package, self.tenant_model.class_name)
