import base64
from os import path

from Minio_OpsHandler.MinioOperationsHandler import MinioOperationsHandler


class ImageEncoderDecoder:
    def __init__(self, config_settings):
        self.config_settings = config_settings
        self.minioOpsHandler = MinioOperationsHandler(config_settings)

    def encode_image(self, image_object_name):
        if self.config_settings is None or self.minioOpsHandler is None:
            # log error
            return None
        bucket_name, object_name, filepath = self.minioOpsHandler.get_object_name(image_object_name)
        if not path.exists(filepath) and not path.isfile(filepath):
            if not self.minioOpsHandler.download_image(image_object_name):
                # log error here -> file not downloaded
                return False
        else:
            with open(filepath, 'rb') as image_file:
                encoded_string = base64.encode(image_file.read())
                return encoded_string
