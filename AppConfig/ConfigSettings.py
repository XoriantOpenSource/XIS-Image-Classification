import configparser
from os.path import isfile


class ConfigSettings:
    def __init__(self):
        self.config_file = "/home/sujit25/Workspace/XIS_App/config.txt"

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
        self.mongo_dbname = None
        self.mongo_collection_name = None


        # google cloud storage settings
        self.gstorage_bucket_name = None
        self.project_id = None

        # setting for which storage location to use (minio or gcp storage)
        self.use_gcp_storage = None

    def read_config_settings(self):
        if not isfile(self.config_file):
            print("config file does not exists")
            return False
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read_file(open(self.config_file))
            self.source_images_location = config_parser["general_settings"]["source_images_location"]
            self.download_location = config_parser["general_settings"]["download_location"]
            self.use_gcp_storage = config_parser["general_settings"]["use_gcp_storage"]
            self.image_files_extensions = config_parser["image_filter"]["image_file_extensions"]

            # read minio server settings
            self.minio_endpoint = config_parser["minio_settings"]["endpoint"]
            self.minio_key = config_parser["minio_settings"]["key"]
            self.minio_secret = config_parser["minio_settings"]["secret"]
            self.minio_bucket_name = config_parser["minio_settings"]["bucket_name"]
            self.minio_prefix = config_parser["minio_settings"]["prefix"]

            # read mongo settings
            self.mongo_host = config_parser["mongo_connection_settings"]["host"]
            self.mongo_port = config_parser["mongo_connection_settings"]["port"]
            self.mongo_collection_name = config_parser["mongo_connection_settings"]["collection_name"]
            self.mongo_dbname = config_parser["mongo_connection_settings"]["db_name"]

            # read gcp storage settings
            self.project_id = config_parser["google_cloud_storage_settings"]["project_id"]
            self.gstorage_bucket_name = config_parser["google_cloud_storage_settings"]["bucket_name"]
            return True

        except:
            print("failed to open config file")
            return False


if __name__ == "__main__":
    configSettings = ConfigSettings()
    configSettings.read_config_settings()
