# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2023/11/21 17:21
import fnmatch
import logging
import os
import subprocess
import time


def exec_shell(command: str):
    """
    :param command:     string      命令
    :return output: string      日志
    :return error: string      错误
    :return returncode: string      返回码
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8'), process.returncode


def check_file(directory: str, filename: str, max_checks: int = 60):
    """
    检测服务器是否有这个文件
    :param directory:           检查的目录
    :param filename:            检查的文件名
    :param max_checks:          最多检测的次数
    """
    checks = 1
    logging.info(f'本次检查{directory}下的{filename}文件，一共检测{max_checks}次')

    while checks < max_checks:
        # 检测文件夹本身是否存在
        if not os.path.exists(directory):
            logging.info(f"当前为第{checks}次尝试，文件夹 {directory} 不存在，等待...")
            time.sleep(5)
            checks += 1
        else:
            # 检测文件是否存在
            files = os.listdir(directory)
            matched_files = [file for file in files if fnmatch.fnmatch(file, filename)]

            if matched_files:
                logging.info(f"当前为第{checks}次尝试，文件 {filename} 存在，继续执行！")
                return True  # 如果文件存在，返回成功
            else:
                logging.info(f"当前为第{checks}次尝试，文件 {filename} 不存在，等待...")
                time.sleep(5)
                checks += 1
    return False  # 达到最大检测次数后返回失败
