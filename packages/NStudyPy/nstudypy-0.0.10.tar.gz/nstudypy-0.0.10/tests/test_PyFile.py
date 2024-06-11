#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-04 16:09
# @Author  : Jack
# @File    : test_PyFile

"""
test_PyFile
"""
from NStudyPy import PyFile

if __name__ == '__main__':
    # PyFile.delete_repeat_file(r'F:\temp\cards\xxxx')
    tag = '职称证'
    PyFile.random_split_s(source_dir=rf'F:\temp\cards\{tag}', target_dir=rf'F:\temp\target\{tag}')
