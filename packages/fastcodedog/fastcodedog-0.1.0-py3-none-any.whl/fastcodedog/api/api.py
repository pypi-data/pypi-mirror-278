# -*- coding: utf-8 -*-
from fastcodedog.context.context_instance import ctx_instance
from fastcodedog.crud.param import Param
from fastcodedog.generation.file import File
from fastcodedog.generation.function_block import FunctionBlock
from fastcodedog.generation.variable import Variable
from fastcodedog.util.case_converter import camel_to_snake
from .app_function import AppFunction
from .oauth import enable_api_oauth2
from ..util.inflect_wrapper import plural


class Api(File):
    def __init__(self, crud, path, package, desc=None):
        super().__init__(path, package, desc)
        self.code = crud.code
        self.crud = crud
        self.schema = self.crud.schema
        self.model = self.schema.model
        self.schema_additional = ctx_instance.schema_additional_package.shcema_additionals.get(self.code)

        # 需要计算属性
        self.response_model = None
        self.response_model_list = None
        self.validate_response_function = None  # 可用于判断是否有多个返回值
        self.extra_function_params = {}  # 额外请求参数，比如session，每个请求中都隐含
        self.extra_function_params_when_get = {}  # get请求的额外参数，比如response_model, session
        self.extra_function_params_when_get_list = {}  # get请求列表的额外参数，比如skip, limit, response_model, session

        # 计算属性
        self._init_import_stmt()
        self._init_variable()  # 会同步计算response_model、response_model_list和validate_response_model
        self._init_properties()
        # 检查是否启用oauth2
        enable_api_oauth2(self)
        self._init_method()

    def _init_method(self):
        for function_block in self.crud.function_blocks.values():
            method = self.get_app_method(function_block.option)
            model_id_name = camel_to_snake(self.model.class_name) + '_id'
            url = f'/{plural(camel_to_snake(self.model.class_name))}' if function_block.return_list else f'/{camel_to_snake(self.model.class_name)}'
            if not function_block.return_list and model_id_name in function_block.params.keys():
                url += '/{' + model_id_name + '}'
            if function_block.query_name:
                url += '/' + camel_to_snake(function_block.query_name)
            elif function_block.schema_additional_name:
                url += '/' + camel_to_snake(function_block.schema_additional_name)
            elif function_block.sub_object_name:
                url += '/' + camel_to_snake(function_block.sub_object_name)
            app_func = AppFunction(function_block.name, self, method, url)
            app_func.params = {k: v for k, v in function_block.params.items() if
                               k not in self.extra_function_params.keys()}
            for k, v in function_block.params.items():
                if k in self.extra_function_params.keys():
                    continue
                app_func.params[k] = Param(k, parent=self, default=v.default, nullable=v.nullable,
                                           type=v.type if not v.schema_class_block else v.schema_class_block.name)

            app_func.content = f'crud.{function_block.name}(' + ', '.join(
                [f'{k}={v.code}' for k, v in function_block.params.items()]) + ')'
            if function_block.return_list:
                app_func.reponse_model = self.response_model_list
                app_func.params.update(self.extra_function_params_when_get_list)
                if self.validate_response_function:
                    app_func.content = f'return [response_model.from_orm({camel_to_snake(self.model.class_name)}) for {camel_to_snake(self.model.class_name)} in {app_func.content}]'
                else:
                    app_func.content = f'return {app_func.content}'
            elif method != 'delete':
                app_func.reponse_model = self.response_model
                app_func.params.update(self.extra_function_params_when_get)
                if self.validate_response_function:
                    app_func.content = f'return response_model.from_orm({app_func.content})'
                else:
                    app_func.content = f'return {app_func.content}'
            else:
                app_func.params.update(self.extra_function_params)
            app_func.content += '\n'
            self.function_blocks[app_func.name] = app_func
            ...

    def get_app_method(self, option):
        if option == 'get':
            return 'get'
        if option == 'create':
            return 'post'
        if option == 'update':
            return 'put'
        if option == 'delete':
            return 'delete'

    def _init_properties(self):
        # 要先初始化_init_variable，确保validate_response_function已经被正确设置
        self.extra_function_params['session'] = Param('session', parent=self, type='Session',
                                                      default='Depends(get_session)')
        if self.validate_response_function:
            self.extra_function_params_when_get['response_model'] = Param('response_model', parent=self,
                                                                          type='BaseModel',
                                                                          default=f'Depends({self.validate_response_function})')
        self.extra_function_params_when_get.update(self.extra_function_params)
        # self.extra_function_params_when_get_list['skip'] = Param('skip', parent=self, type='int', default=0)
        # self.extra_function_params_when_get_list['limit'] = Param('limit', parent=self, type='int', default=50)
        self.extra_function_params_when_get_list.update(self.extra_function_params_when_get)

    def _init_variable(self):
        self.variables['app'] = Variable('app', parent=self, default='FastAPI()')
        response_class_blocks = []
        for class_block in self.schema.class_blocks.values():
            if class_block.method == 'response':
                response_class_blocks.append(class_block)
        # 所有的schema_additional
        if self.schema_additional:
            for class_block in self.schema_additional.class_blocks.values():
                if class_block.method == 'response':
                    response_class_blocks.append(class_block)
        if len(response_class_blocks) == 1:
            self.response_model = response_class_blocks[0].name
            self.response_model_list = f'list[{response_class_blocks[0].name}]'
        elif len(response_class_blocks) > 1:
            self.response_model = f'ALL_{self.model.class_name.upper()}_RESPONSE_MODEL'
            self.response_model_list = f'ALL_{self.model.class_name.upper()}_LIST_RESPONSE_MODEL'
            self.variables[self.response_model] = Variable(self.response_model, parent=self, type='Union',
                                                           default=f'Union[{", ".join([response_class_block.name for response_class_block in response_class_blocks])}]')
            self.variables[self.response_model_list] = Variable(self.response_model_list, parent=self, type='Union',
                                                                default=f'Union[{", ".join(["list[" + response_class_block.name + "]" for response_class_block in response_class_blocks])}]')
            self._add_validate_response_model_function(response_class_blocks)

    def _add_validate_response_model_function(self, response_class_blocks):
        function_name = f'validate_{self.model.class_name.lower()}_response_model'
        function = FunctionBlock(function_name, parent=self)
        request_allow = [f"'{camel_to_snake(response_class_block.name)}'" for response_class_block in
                         response_class_blocks]
        param_default = f"Query(None, description=\"指定返回的数据类型，默认为'{camel_to_snake(self.model.class_name)}'\", enum=[{', '.join(request_allow)}])"
        function.params['response_model'] = Param('response_model', parent=function, type='str', default=param_default)
        function.content = f"""if response_model and response_model not in [{', '.join(request_allow)}]:
    raise HTTPException(status_code=400,
        detail="Invalid response_model. Must in {', '.join(request_allow)}.")
"""
        for class_block in response_class_blocks:
            function.content += f"if response_model == '{camel_to_snake(class_block.name)}':\n"
            function.content += f"    return {class_block.name}\n"
        function.content += f"return {self.model.class_name}\n"

        self.validate_response_function = function_name
        self.function_blocks[function_name] = function

    def _init_import_stmt(self):
        self.import_stmt.add_import('fastapi', 'FastAPI')
        self.import_stmt.add_import('fastapi', 'Depends')
        self.import_stmt.add_import('pydantic', 'BaseModel')
        self.import_stmt.add_import(ctx_instance.base.package, ctx_instance.base.class_name)
        self.import_stmt.add_import(f'{ctx_instance.project_package}.db', 'Session')
        self.import_stmt.add_import(f'{ctx_instance.project_package}.db', 'get_session')
        self.import_stmt.add_import(from_=None, import_=self.crud.package, as_='crud')
        response_model_count = 0
        # 所有的schema
        for class_block in self.schema.class_blocks.values():
            if class_block.method in ['response', 'create', 'update']:
                self.import_stmt.add_import(self.schema.package, class_block.name)
                for attribute in class_block.attributes.values():
                    if attribute.nullable:
                        self.import_stmt.add_import('typing', 'Optional')
                if class_block.method == 'response':
                    response_model_count += 1
        # 所有的schema_additional
        if self.schema_additional:
            for class_block in self.schema_additional.class_blocks.values():
                self.import_stmt.add_import(self.schema_additional.package, class_block.name)
                for attribute in class_block.attributes.values():
                    if attribute.nullable:
                        self.import_stmt.add_import('typing', 'Optional')
                if class_block.method == 'response':
                    response_model_count += 1
        if response_model_count > 1:
            self.import_stmt.add_import('typing', 'Union')
            self.import_stmt.add_import('fastapi', 'Query')
            self.import_stmt.add_import('fastapi', 'HTTPException')
