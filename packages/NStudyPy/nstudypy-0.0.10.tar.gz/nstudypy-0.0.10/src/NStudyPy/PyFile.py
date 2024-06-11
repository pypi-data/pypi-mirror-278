#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-28 14:13
# @Author  : Jack
# @File    : PyFile

"""
PyFile
"""
import os
import random
import shutil
import hashlib


def check_file_ext(filename: str, allowed_extensions=['png', 'jpg', 'jpeg']) -> bool:
    """
    检查文件扩展名是否符合要求
    :param filename:
    :param allowed_extensions:
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def makedirs(path: str, is_file: bool = True):
    """
    创建目录
    :param is_file: 是否是文件
    :param path:
    :return:
    """
    if is_file:
        path = os.path.dirname(path)
    os.makedirs(path, exist_ok=True)


def get_filename(file_path: str) -> str:
    """
    获取文件名
    :param file_path: 是否是文件
    :return: 文件名
    """
    return os.path.basename(file_path)


def random_split_s(source_dir: str, target_dir: str, s=(100, 400, 250, 250)) -> None:
    """
    随机拆分文件; 不处理子文件夹
    :param source_dir: 源文件夹
    :param target_dir: 目标文件夹
    :param s: 拆分个数 (100, 400, 250, 250) 是每个分组的个数，直至所有文件都拆分完毕
    :return: None
    """
    files = os.listdir(source_dir)
    random.shuffle(files)

    sum_s = 0
    for idx, count in enumerate(s):
        _no = f'{idx:03}'
        image_g_dir = os.path.join(target_dir, _no)
        if not os.path.exists(image_g_dir):
            os.makedirs(image_g_dir)
        for file_name in files[sum_s:sum_s + count]:
            shutil.copy(os.path.join(source_dir, file_name), os.path.join(image_g_dir, file_name))
        sum_s += count
        if sum_s >= len(files):
            break
    # Done it


def random_spilt(source_dir: str, target_dir: str, spilt_count=200) -> None:
    """
    把一个文件夹的文件,随机分成 spilt_count 一个文件夹 ; 不处理子文件夹
    :param source_dir: 源文件夹
    :param target_dir: 目标文件夹
    :param spilt_count: 每个文件夹的文件数量
    :return: None
    """
    files = os.listdir(source_dir)

    random.shuffle(files)

    # group_files_len = (len(files) + spilt_count - 1) // spilt_count

    group_files = [files[i:i + spilt_count] for i in range(0, len(files), spilt_count)]
    for idx, g in enumerate(group_files):
        _no = f'{idx:03}'
        image_g_dir = os.path.join(target_dir, _no)
        if not os.path.exists(image_g_dir):
            os.makedirs(image_g_dir)
        for i in g:
            shutil.copy(os.path.join(source_dir, i), os.path.join(image_g_dir, i))


def get_file_list(path: str, is_recursive=True) -> list:
    """
    获取文件列表
    :param path: 路径
    :param is_recursive: 是否递归
    :return: 文件列表
    """
    if not os.path.exists(path):
        raise FileNotFoundError('Path does not exist')
    if os.path.isdir(path):
        files = []
        for root, _, f_names in os.walk(path):
            for f_name in f_names:
                files.append(os.path.join(root, f_name))
            if not is_recursive:
                break
    else:
        files = [path]
    return files


def get_md5(file_path) -> str:
    """
    获取文件的md5值
    :param file_path: 文件路径
    :return: md5值
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError('Path does not exist')
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_repeat_file(path: str, is_recursive=True) -> dict:
    """
    获取重复文件
    :param path: 路径
    :param is_recursive:  是否递归
    :return: dict {"md5" : [file1,file2]}
    """
    file_dict = dict()
    for f in get_file_list(path, is_recursive):
        md5 = get_md5(f)
        if md5 not in file_dict:
            file_dict[md5] = [f]
        else:
            file_dict[md5].append(f)
    repeat_files = dict()
    for k, v in file_dict.items():
        if len(v) > 1:
            repeat_files.update({k: v})
            print(f'{k} {len(v)}')
    # return list(filter(lambda x: len(x) > 1, file_dict.values()))
    return repeat_files


def delete_repeat_file(path: str, is_recursive=True) -> None:
    """
    删除重复文件
    :param path: 路径
    :param is_recursive:  是否递归
    :return: None
    """
    for f in get_repeat_file(path, is_recursive).values():
        for i in f[1:]:
            os.remove(i)
