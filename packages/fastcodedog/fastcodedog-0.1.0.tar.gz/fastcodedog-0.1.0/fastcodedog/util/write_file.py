# -*- coding: utf-8 -*-
"""
@author: hubo
@project: fastframe
@file: write_file
@time: 2024/5/30 15:39
@desc:
"""

import subprocess


def write_python_file(path, content):
    """
    写入python文件
    :param path:
    :param content:
    :return:
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    # 调用autopep8格式化文件
    # subprocess.run(['autopep8', '--in-place', '--aggressive', '--max-line-length=120', path], check=True)
    subprocess.run(['autopep8', '--in-place', '--max-line-length=120', path], check=True)
    # # 调用flake8格式化文件
    # subprocess.run(['flake8', path], check=True)
