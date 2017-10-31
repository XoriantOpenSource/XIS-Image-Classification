import io
from os import listdir
from os.path import basename, splitext
from os.path import isdir, join, isfile

from google.cloud import vision
from google.cloud.vision import types

from AppConfig.ConfigSettings import ConfigSettings
from GCP_StorageOpsHandler.GCP_StorageOpsHandler import GCPStorageCrud
from Minio_OpsHandler.MinioOperationsHandler import MinioOperationsHandler
from Mongodb_OpsHandler.DbOperationsHandler import DbOperationsHandler


class ImageIndexer:
    def __init__(self, config_setting):
        self.config_settings = config_setting
        self.client = vision.ImageAnnotatorClient()
        self.gcp_storage_handler = None
        self.minio_ops_handler = None

        self.db_operations_handler = DbOperationsHandler(config_setting)
        if config_setting.use_gcp_storage:
            self.gcp_storage_handler = GCPStorageCrud(app_config_settings=config_setting)
        else:
            self.minio_ops_handler = MinioOperationsHandler(config_setting=config_setting)
            self.minio_ops_handler.init_minio_handler()
            # print(self.client)

    def get_image_files(self, dir_path):
        if not isdir(dir_path):
            return None
        image_extensions = list(self.config_settings.image_files_extensions)

        # get image file paths with match filter criteria
        image_files = [join(dir_path, image_file) for image_file in listdir(dir_path) if
                       isfile(join(dir_path, image_file)) and
                       any(image_file.endswith(ext) for ext in image_extensions)]
        return image_files

    def get_image_labels(self, image_file_path):
        # load image into memory
        with io.open(image_file_path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

        # get labels
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        # print(labels)

        filtered_labels = [label.description for label in labels if label.score >= 0.65]
        return filtered_labels

    def classify_images(self, image_files):
        if not image_files:
            return
        for index, image_file_path in enumerate(image_files):
            self.process_image(image_file_path, index)
            # log image file processing status here with file name

    def process_image(self, image_file_path, index):
        labels = self.get_image_labels(image_file_path)

        if self.config_settings.use_gcp_storage:
            op_status = self.gcp_storage_handler.upload_image(image_file_path)
            image_object_name = self.gcp_storage_handler.bucket_name + "_" + self. \
                get_file_name(image_file_path, include_extension=True)
        else:
            op_status = self.minio_ops_handler.upload_image(image_file_path)
            image_object_name = self.minio_ops_handler.bucket_name + "_" + self. \
                get_file_name(image_file_path, include_extension=True)

        if op_status and image_object_name and self.db_operations_handler:
            image_document = {
                'image_object_name': image_object_name,
                'labels': labels
            }
            return self.db_operations_handler.insert_image(image=image_document)
        else:
            return False

    @staticmethod
    def get_file_name(file_path, include_extension=False):
        return basename(file_path) if include_extension else splitext(basename(file_path))[0]

    def search_images(self, query):
        if not query:
            return None
        query_results = self.db_operations_handler.search_by_labels(query)
        for query_result in query_results:
            self.gcp_storage_handler.download_image(query_result) if self.config_settings.use_gcp_storage \
                else self.minio_ops_handler.download_image(query_result)

    def index_images(self):
        if not (self.config_settings.source_images_location and isdir(self.config_settings.source_images_location)):
            print("source image directory doesn't exists")
            return False
        images = self.get_image_files(self.config_settings.source_images_location)
        self.classify_images(images)

    def search_by_query(self, search_query):
        if not (self.config_settings.download_location and isdir(self.config_settings.download_location)):
            print("download directory doesn't exists")
            return False
        self.search_images(search_query)


if __name__ == "__main__":
    # source_images_location = "/home/sujit25/Workspace/MinioPython/GoogleCloudVisionExamples/resources"
    # download_location = "/home/sujit25/Workspace/MinioPython/GoogleCloudVisionExamples/downloads"

    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        indexer = ImageIndexer(config_settings)
        # indexing
        indexer.index_images()

        # search and download results
        # search_query = ['cat', 'dog']
        # labels = indexer.search_by_query(search_query)
        # print()

# db.createUser({user:'sujit25',pwd:'sujit25', roles:[{role:'dbAdmin',db:'image_metadata'}]})
