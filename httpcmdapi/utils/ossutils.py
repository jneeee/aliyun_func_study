# -*- coding: utf-8 -*-
import oss2
import os
import pickle


class OssFileClient():
    def __init__(self):
        auth = oss2.Auth(os.environ.get('aliyun_ramkey'), os.environ.get('aliyun_ramkeysec'))
        # TODO 确认 internal ep是否正常
        self.bucket = oss2.Bucket(auth, os.environ.get('aliyun_ramkey'), 
                                  os.environ.get('aliyun_bucketname'))

    def queue(self, path, key):
        self.bucket.get_object_to_file(path, 'D:\\localpath\\examplefile.txt')   
        # TODO get file in memory
        return

    def put(self, path, key, file):
        with open(file, 'rb') as fileobj:
            self.bucket.put_object('exampleobject.txt', fileobj)


class nasclient():

    def __init__(self, table='db/default/'):
        self.pre_path = f'/home/ubuntu/{table}'
        print(f'init {self.pre_path} success!')
        if not os.path.exists(self.pre_path):
            os.makedirs(self.pre_path)

    def save(self, data, filename=None):
        path = f'{self.pre_path}{filename}'
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f'store file: {path} success!')

    def load(self, filename):
        path = f'{self.pre_path}{filename}'
        with open(path, 'rb') as f:
            res = pickle.load(f)
        print('Read file {path}: {res}')
        return res

    def ls(self, path=None):
        res = None
        if not path:
            res = os.listdir(self.pre_path) 
        elif os.path.exists(path):
            res = os.listdir(path)
        return res

