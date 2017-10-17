import base64
from os import path

from AppConfig.ConfigSettings import ConfigSettings
from Minio_OpsHandler.MinioOperationsHandler import MinioOperationsHandler


class ImageEncoderDecoder:
    def __init__(self, config_settings):
        self.config_settings = config_settings
        self.minio_ops_handler = MinioOperationsHandler(config_settings)

    def encode_image(self, image_object_name):
        if self.config_settings is None or self.minio_ops_handler is None:
            # log error
            return ""
        bucket_name, object_name, file_path = self.minio_ops_handler.get_object_name(image_object_name)
        if not path.exists(file_path) and not path.isfile(file_path):
            if not self.minio_ops_handler.download_image(image_object_name):
                # log error here -> file not downloaded
                return ""
        return self.encode_image_string(file_path)

    def encode_image_string(self, file_path):
        try:
            with open(file_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('ascii')
                return encoded_string
        except FileNotFoundError:
            return ""


if __name__ == "__main__":
    config_setting = ConfigSettings()
    if config_setting.read_config_settings():
        image_encoderDecoder = ImageEncoderDecoder(config_setting)
        image_encodingResult = image_encoderDecoder.encode_image('xis-images_cheetah1.jpg')
        if not image_encodingResult:
            print("failed to encode image")
        else:
            print("encoded image successfully")
            print("encoded string:" + image_encodingResult)
