import json
from os.path import exists,isfile
#from image_indexer.AppConfig import AppConfigSettings


class AppConfigSettings:
    def __init__(self):
        self.config_file = "/home/sujit25/Workspace/XIS_commandline_app/image_indexer/AppConfig/config.json"

        # general settings
        self.source_images_location = None
        self.download_location = None
        self.image_files_extensions = None

        # minio settings
        self.minio_endpoint = None
        self.minio_port = None
        self.minio_secret = None
        self.minio_bucket_name = None
        self.minio_prefix = None

        # mongo settings
        self.mongo_host = None
        self.mongo_port = None

    def read_config_settings(self):
        if not isfile(self.config_file):
            print("config file does not exists")
            return False

        try:
            with open(self.config_file) as json_config:
                data = json.load(json_config)
                print(data)
                # read general settings
                self.source_images_location = data["general_settings"]["source_images_location"]
                self.download_location = data["general_settings"]["download_location"]
                self.image_files_extensions = data["image_filter"]["image_file_extensions"]

                # read minio server settings
                self.minio_endpoint = data["minio_settings"]["endpoint"]
                self.minio_key = data["minio_settings"]["key"]
                self.minio_secret = data["minio_settings"]["secret"]
                self.minio_bucket_name = data["minio_settings"]["bucket_name"]
                self.minio_prefix = data["minio_settings"]["prefix"]

                #read mongo settings
                self.mongo_host = data["mongo_connection_settings"]["host"]
                self.mongo_port = data["mongo_connection_settings"]["port"]
                return True
        except ValueError as valueEx:
                # log exception here
                print("config file is not a valid json")
                return False
        except Exception as ex:
                # log error here
                print("error occurred while reading config file")
                return False

if __name__ == "__main__":
    configSettings = AppConfigSettings()
    opStatus = configSettings.read_config_settings()
    print(opStatus)