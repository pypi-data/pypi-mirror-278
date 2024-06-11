# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/11/1 
# @Function:
import base64
import hashlib
from pathlib import Path

import shutil


def overwrite_folder(from_dir: Path, to_dir: Path):
    """
    覆盖目录，覆盖已有文件
    :param from_dir: 目录
    :param to_dir: 被覆盖目录
    :return:
    """
    for file in from_dir.rglob("*.*"):
        shutil.copy(file, to_dir.joinpath(file.parent.name))
        print(file)
    pass


def md5(file_path: Path):
    """
    文件转md5
    :param file_path: 文件路径
    """
    with file_path.open('rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def get_base64(file_path: Path, contain_file_name=False, split_char=","):
    """
    文件转base64
    :param file_path: 文件路径
    :param contain_file_name: 是否包含文件名称
    :param split_char: 分隔符
    :return: 'a.jpg,iVBORw0KGgoAAAANSUhEUgAABNcAAANtCAYAAACzHZ25AAA.....'
    """
    with file_path.open('rb') as infile:
        s = infile.read()
    base64_str = base64.b64encode(s).decode("utf-8")
    if contain_file_name:
        base64_str = file_path.name + split_char + base64_str
    return base64_str
