# -*- coding: utf-8 -*-
"""
jfExt.fileExt.py
~~~~~~~~~~~~~~~~

:copyright: (c) 2018-2022 by the Ji Fu, see AUTHORS for more details.
:license: MIT, see LICENSE for more details.
"""

from icecream import ic # noqa
import xlwt
import os
import time
import hashlib


# pragma mark - Private
# --------------------------------------------------------------------------------
def TimeStampToTime(timestamp):
    '''
    >>> 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    '''
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


# pragma mark - Public
# --------------------------------------------------------------------------------
def file_get_file_size(file_path):
    '''
    >>> 获取文件的大小,结果保留两位小数, 单位为MB
    '''
    file_path = file_path.encode('utf8')
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def file_get_file_accesstime(file_path):
    '''
    >>> 获取文件的访问时间
    '''
    file_path = file_path.encode('utf8')
    t = os.path.getatime(file_path)
    return TimeStampToTime(t)


def file_get_file_createtime(file_path):
    '''
    >>> 获取文件的创建时间
    '''
    file_path = file_path.encode('utf8')
    t = os.path.getctime(file_path)
    return TimeStampToTime(t)


def file_get_file_modifytime(file_path):
    '''
    >>> 获取文件的修改时间
    '''
    file_path = file_path.encode('utf8')
    t = os.path.getmtime(file_path)
    return TimeStampToTime(t)


def file_get_file_md5(file_path):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()       # 创建md5对象
    with open(file_path, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象
    return m.hexdigest()    # 返回md5对象


# pragma mark - EXCEL
# --------------------------------------------------------------------------------
def excel_gen_by_dict(file_path, titles, data_dict):
    """
    >>> excel导出到文件
    :param {String} file_path: 目标文件路径
    :param {List} titles: 标题列表
    :param {Dictionary} data_dict: 数据
    :return {String}: 保存文件的路径
    """
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    t = 1
    for i in range(len(titles)):
        title = titles[i]
        booksheet.write(0, i, title)
    for product in data_dict:
        for i in range(len(titles)):
            title = titles[i]
            value = product.get(title, '')
            if isinstance(value, dict) or isinstance(value, list):
                continue
            booksheet.write(t, i, value)
        t += 1
    workbook.save(file_path)
    return file_path
