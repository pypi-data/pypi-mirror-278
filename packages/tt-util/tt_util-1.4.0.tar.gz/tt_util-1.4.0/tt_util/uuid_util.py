# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/12/15 10:17
import logging
from typing import Union, List


def edit_uuid(uuid_filename: Union[str, List[str]]):
    """
    把uuid的第一个值提取出来，做一层文件夹，可以让oss上快速查询
    :param uuid_filename: uuid filename
    :return: 解析后的filename
    """
    if isinstance(uuid_filename, str):
        first_part = uuid_filename.split('-')[0]
        uuid_url = first_part + '/' + uuid_filename
        return uuid_url
    elif isinstance(uuid_filename, List):
        uuid_url = []
        for i in range(len(uuid_filename)):
            first_part = uuid_filename[i].split('-')[0]
            uuid_url.append(first_part + '/' + uuid_filename[i])
        return uuid_url
    else:
        logging.error('入参类型不对')
        return ''


def edit_url(uuid_url: Union[str, List[str]]):
    """
    把第一层文件夹给去掉
    :param uuid_url: uuid url
    :return: 解析后的filename
    """
    if isinstance(uuid_url, str):
        file_name = uuid_url.split('/')[-1]
        return file_name
    elif isinstance(uuid_url, List):
        for i in range(len(uuid_url)):
            uuid_url[i] = uuid_url[i].split('/')[-1]
        return uuid_url
    else:
        logging.error('入参类型不对')
        return ''
