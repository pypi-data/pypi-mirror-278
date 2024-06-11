# -*- coding: utf-8 -*-            
# @Author : buyfakett
# @Time : 2024/2/19 9:50
import oss2


class AliyunOSS:
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)

    def upload_object(self, object_key, file_path):
        """
        上传文件
        :param object_key: 上传后的名称
        :param file_path: 上传的本地路径
        """
        with open(file_path, 'rb') as fileobj:
            self.bucket.put_object(object_key, fileobj)

    def download_object(self, object_key, local_file_path):
        """
        下载对象到本地文件
        :param local_file_path: 本地文件路径
        """
        self.bucket.get_object_to_file(object_key, local_file_path)

    def delete_object(self, object_key):
        """
        删除文件
        :param object_key: 目录路径
        """
        self.bucket.delete_object(object_key)

    def list_files_in_directory(self, directory_path=''):
        """
        返回指定目录下的文件列表
        :param directory_path: 目录路径，默认为空字符串表示根目录
        """
        if directory_path and not directory_path.endswith('/'):
            directory_path += '/'

        objects = []
        for obj in oss2.ObjectIterator(self.bucket, delimiter='/', prefix=directory_path):
            if obj.is_prefix():
                continue
            objects.append(obj.key)
        return objects