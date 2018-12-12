import os, oss2

ACCESSKEY_ID= 'LTAIZOsLduV58VgI'
ACCESSKEY_SECRET = '1n06hOqorAao9Uy0zlTs5CGniCX1sN'
HOST = 'http://oss-cn-shenzhen.aliyuncs.com'
BUCKET = 'test0705'
DOWNLOAD_DIR = './download'

class DownloadService():

    def __init__(self):
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

    def download_file_from_oss(self, file_path):
        auth = oss2.Auth(ACCESSKEY_ID, ACCESSKEY_SECRET)
        bucket = oss2.Bucket(auth, HOST, BUCKET)

        store_dir = DOWNLOAD_DIR + '/' + self.get_dir_from_file_path(file_path)
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)

        store_path = DOWNLOAD_DIR + '/' + file_path
        bucket.get_object_to_file(file_path, store_path)
        return store_path

    def get_dir_from_file_path(self, file_path):
        return file_path[0:file_path.rindex('/')]