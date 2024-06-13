# -*- coding: utf-8 -*-
from fastcodedog.generation.function_block import FunctionBlock
from fastcodedog.util.indent import add_indent


class AppFunction(FunctionBlock):
    def __init__(self, name, parent, method, url, reponse_model=None, response_model_exclude_none=True, params=None):
        super().__init__(name, parent, params)
        self.method = method
        self.url = url
        self.reponse_model = reponse_model
        self.response_model_exclude_none = response_model_exclude_none

    def serialize(self, indent=''):
        app_params = [f"'{self.url}'"]
        if self.reponse_model:
            app_params.append(f'response_model={self.reponse_model}')
            if self.response_model_exclude_none:
                app_params.append('response_model_exclude_none=True')
        content = f'@app.{self.method}({", ".join(app_params)})\n'
        content += super().serialize()
        return add_indent(content, indent)
