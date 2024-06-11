#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-04 15:21
# @Author  : Jack
# @File    : test_LabelStudio

"""
test_LabelStudio
"""

from NStudyPy import PyEnv, PyLabelStudio

if __name__ == '__main__':
    _file_paths = [
        r'C:\Users\lizhiquan\Downloads\project-13-at-2024-06-11-07-24-0824dc98.json'
    ]

    PyLabelStudio.convert_to_UIEX(file_paths=_file_paths, main_dir=r'E:\Projects\pp-uiex-certs\data', domain=PyEnv.get_env('ls_domain'), auth=PyEnv.get_env('ls_auth'))

    # PyLabelStudio.stat_label(file_paths=_file_paths)
