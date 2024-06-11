#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .yaml_util import read_yaml

from qiniu import put_file, Auth, BucketManager, build_batch_delete


class QiniuFunction(object):
    def __init__(self, access_key=read_yaml('access_key', 'config'), secret_key=read_yaml('secret_key', 'config'),
                 bucket=str(read_yaml('bucket_name', 'config'))):
        self.bucket = bucket
        self.q = Auth(access_key, secret_key)
        self.domain = read_yaml('domain', 'config')

    def upload_file(self, local_file, remote_file):
        # 上传后保存的文件名
        token = self.q.upload_token(self.bucket, remote_file, 999999)
        ret, info = put_file(token, remote_file, local_file, version='v2')
        return ret, info

    def download_file(self, remote_file):
        # 有两种方式构造base_url的形式
        base_url = 'https://%s/%s' % (self.domain, remote_file)
        # private_url = self.q.private_download_url(base_url, expires=3600)
        return base_url

    def delete_file(self, remote_file):
        bucket_manager = BucketManager(self.q)
        ret, info = bucket_manager.delete(self.bucket, remote_file)
        return ret, info

    def delete_files(self, remote_files):
        bucket_manager = BucketManager(self.q)
        ops = build_batch_delete(self.bucket, remote_files)
        ret, info = bucket_manager.batch(ops)
        return ret, info
