import base64
from os import path

from XIS_RestApi.AppConfig.ConfigSettings import ConfigSettings

from XIS_RestApi.Minio_OpsHandler import MinioOperationsHandler


class ImageEncoderDecoder:
    def __init__(self, config_settings):
        self.config_settings = config_settings
        self.minioOpsHandler = MinioOperationsHandler(config_settings)

    def encode_image(self, image_object_name):
        if self.config_settings is None or self.minioOpsHandler is None:
            # log error
            return ""
        bucket_name, object_name, filepath = self.minioOpsHandler.get_object_name(image_object_name)
        if not path.exists(filepath) and not path.isfile(filepath):
            if not self.minioOpsHandler.download_image(image_object_name):
                # log error here -> file not downloaded
                return ""
        return self.encode_image_string(filepath)

    def encode_image_string(self,filepath):
        try:
            with open(filepath, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('ascii')
                return encoded_string
        except FileNotFoundError as fileError:
            # log error -> file not found
            return ""
        except Exception as ex:
            return ""

if __name__ == "__main__":
    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        image_encoderDecoder = ImageEncoderDecoder(config_settings)
        image_encodingResult = image_encoderDecoder.encode_image('xis-images_cheetah1.jpg')
        if not image_encodingResult:
            print("failed to encode image")
        else:
            print("encoded image successfully")
            print("encoded string:" + image_encodingResult)
