# -*- coding: utf-8 -*-

from fastcodedog.context.context_instance import ctx_instance


def test_c():
    ctx_instance.load_config('fastcodedog/test/fastcodedog.*.json5')
    ...
