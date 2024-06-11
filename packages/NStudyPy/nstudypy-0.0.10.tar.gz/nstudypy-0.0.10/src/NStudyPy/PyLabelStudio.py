#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-13 15:48
# @Author  : Jack
# @File    : PyLabelStudio

"""
PyLabelStudio
"""
import json
import os

from NStudyPy import PyString, PyWeb


def convert_to_UIEX(file_paths: [str], main_dir='./data', domain=None, auth=None) -> None:
    """
    将LabelStudio的json文件转换为UIEX格式
    :param file_paths: 文件路径列表
    :param main_dir: 文件保存目录
    :param domain: 图片域名
    :param auth: 网站授权
    :return: None
    """
    _list = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                project_id = item["project"]
                task_id = item["id"]
                data_image = item["data"].get("image")

                annotation = item["annotations"][0]
                task_completion_id = annotation["id"]
                new_image_name = f'{project_id}_{task_id}_{task_completion_id}_{str(item["file_upload"]).replace("-", "_")}'
                image_path = os.path.join(main_dir, 'images', new_image_name)
                if not os.path.exists(image_path):
                    if domain is None:
                        raise Exception('domain or auth is None')
                    PyWeb.save_file_from_url(f'{domain}{data_image}', image_path,
                                             {
                                                 "Authorization": f"Token {auth}"
                                             })
                # for ann in annotation['result']:
                #    pass
                item["data"]["image"] = new_image_name
                _list.append(item)
    if len(_list) > 0:
        json_str = json.dumps(_list, indent=4, ensure_ascii=False)
        with open(os.path.join(main_dir, 'label_studio.json'), "w", encoding='utf8') as f:
            f.write(json_str)


def stat_label(file_paths: [str]) -> dict:
    """
    统计标签数量
    :param file_paths: 文件路径列表
    :return: 标签数量字典
    """
    map_stat = {}
    for p in file_paths:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                for ann in item["annotations"][0]['result']:
                    if ann['type'] == 'rectanglelabels':
                        label = ann['value']['rectanglelabels'][0]
                        v = map_stat.get(label)
                        if v is None:
                            map_stat.update({label: 1})
                        else:
                            map_stat.update({label: v + 1})

    print(f'{"no":2}\t{"label":30}\t\t{"count/per":10} ')
    no = 1
    for k, v in sorted(map_stat.items(), key=lambda x: x[1]):
        print(f'{no:2}\t{PyString.pad_string(k, 30)}\t{v:10}')
        no += 1
    return map_stat


def get_real_points(ann):
    """
    get real points from annotation
    :param ann: label studio annotation
    :return: real points array
    """
    if 'original_width' not in ann or 'original_height' not in ann:
        return None
    w, h = ann['original_width'], ann['original_height']
    points = ann['value']['points']
    if points:
        return [[w * point[0] / 100.0, h * point[1] / 100.0] for point in points]
    return None


def convert_to_box(ann):
    """
    转换标注格式
    :param ann: 标注信息
    :return: [x, y, w, h]
    """
    if 'original_width' not in ann or 'original_height' not in ann:
        return None
    value = ann['value']
    w, h = ann['original_width'], ann['original_height']
    if all([key in value for key in ['x', 'y', 'width', 'height']]):
        x, y, w, h = w * value['x'] / 100.0, h * value['y'] / 100.0, w * value['width'] / 100.0, h * value['height'] / 100.0
        return [int(x), int(y), int(x + w), int(y + h)]
    return None
