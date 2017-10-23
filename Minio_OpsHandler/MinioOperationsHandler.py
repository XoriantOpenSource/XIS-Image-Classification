from os.path import basename, splitext
from os.path import isdir, join

import minio
from minio import error
from minio import policy


class MinioOperationsHandler:
    def __init__(self, config_setting):
        self.config_settings = config_setting
        self.endpoint = self.config_settings.minio_endpoint
        self.key = self.config_settings.minio_key
        self.secret = self.config_settings.minio_secret
        self.bucket_name = self.config_settings.minio_bucket_name
        self.prefix = self.config_settings.minio_prefix
        self.minio_client = None
        self.include_file_extension = True

    def init_minio_handler(self):
        try:
            self.minio_client = self.get_client()
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
                self.minio_client.set_bucket_policy(bucket_name=self.bucket_name,
                                                    prefix=self.prefix,
                                                    policy_access=policy.Policy.READ_WRITE)
            return True
        except (error.BucketAlreadyOwnedByYou, error.ResponseError):
            # log exception here
            return False

    def get_client(self):
        return minio.Minio(endpoint=self.endpoint, access_key=self.key, secret_key=self.secret, secure=True)

    def check_status(self):
        if self.minio_client is None:
            self.minio_client = self.get_client()

    def check_object_existence(self, obj_name):
        self.check_status()
        return any(image_object.object_name is obj_name for image_object in
                   self.minio_client.list_objects(bucket_name=self.bucket_name, prefix=self.prefix, recursive=True))

    @staticmethod
    def get_file_name(file_path, include_extension=False):
        return basename(file_path) if include_extension else splitext(basename(file_path))[0]

    def upload_image(self, image_file):
        self.check_status()
        try:
            object_name = self.get_file_name(file_path=image_file, include_extension=self.include_file_extension)
            if not self.check_object_existence(object_name):
                self.minio_client.fput_object(bucket_name=self.bucket_name, object_name=object_name,
                                              file_path=image_file)
            return True
        except error.ResponseError:
            # log error here
            return False

    def download_image(self, image_object_name):
        if not (image_object_name and isdir(self.config_settings.download_location)):
            return None
        self.check_status()
        try:
            bucket_name, object_name = image_object_name.split('_')
            if bucket_name and object_name:
                self.minio_client.fget_object(bucket_name=bucket_name, object_name=object_name,
                                              file_path=join(self.config_settings.download_location, object_name))
                return True
            return False
        except error.ResponseError:
            print("failed to download file")
            return False
            # log error here

