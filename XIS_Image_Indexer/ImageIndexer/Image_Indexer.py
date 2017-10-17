import io
from os import listdir
from os.path import basename, splitext
from os.path import isdir, join, isfile

from AppConfig.ConfigSettings import ConfigSettings
from GCP_StorageOpsHandler.GCP_StorageOpsHandler import GCP_Storage_Crud
from Mongodb_OpsHandler.DbOperationsHandler import DbOperationsHandler
from google.cloud import vision
from google.cloud.vision import types

from Minio_OpsHandler.MinioOperationsHandler import MinioOperationsHandler


class ImageIndexer:
    def __init__(self, configSettings):
        self.config_settings = configSettings
        self.client = vision.ImageAnnotatorClient()
        self.gcp_storage_handler = None
        self.minioOpHandler= None

        self.dbOperationsHandler = DbOperationsHandler(configSettings)
        if configSettings.use_gcp_storage:
            self.gcp_storage_handler = GCP_Storage_Crud(appConfigSettings=configSettings)
        else:
            self.minioOpHandler = MinioOperationsHandler(configSettings=configSettings)
            self.minioOpHandler.init_minio_handler()
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
        if len(image_files) == 0 or image_files is None:
            return
        for image_file_path in image_files:
            status = self.process_image(image_file_path)
            # log image file processing status here with file name

    def process_image(self, image_file_path):
        labels = self.get_image_labels(image_file_path)
        op_status = False
        image_object_name = None

        if self.config_settings.use_gcp_storage:
            op_status = self.gcp_storage_handler.upload_image(image_file_path)
            image_object_name = self.gcp_storage_handler.bucket_name + "_"+ self.get_file_name(
                image_file_path, include_extension=True)
        else:
            op_status =self.minioOpHandler.upload_image(image_file_path)
            image_object_name = self.minioOpHandler.bucket_name + "_" + self.get_file_name(
                image_file_path, include_extension=True)

        if op_status is True and image_object_name is not None and self.dbOperationsHandler is not None:
            image_document = {
                'image_object_name': image_object_name,
                'labels': labels
            }
            return self.dbOperationsHandler.insert_image(image=image_document)
        else:
            return False

    @staticmethod
    def get_file_name(filepath, include_extension=False):
        return basename(filepath) if include_extension else splitext(basename(filepath))[0]

    def search_images(self, query):

        if query is None:
            return None
        query_results = self.dbOperationsHandler.search_by_labels(query)
        for query_result in query_results:
            self.minioOpHandler.download_image(query_result, download_location=self.config_settings.download_location)

    def index_images(self):
        if self.config_settings.source_images_location is None or not isdir(self.config_settings.source_images_location):
            print("source image directory doesn't exists")
            return False
        images = self.get_image_files(self.config_settings.source_images_location)
        self.classify_images(images)

    def search_by_query(self, search_query):
        if self.config_settings.download_location is None or not isdir(self.config_settings.download_location):
            print("download directory doesn't exists")
            return False
        self.search_images(search_query)


def main():
    #source_images_location = "/home/sujit25/Workspace/MinioPython/GoogleCloudVisionExamples/resources"
    #download_location = "/home/sujit25/Workspace/MinioPython/GoogleCloudVisionExamples/downloads"

    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        indexer = ImageIndexer(config_settings)
        # indexing
        indexer.index_images()

        # search and download results
        #search_query = ['cat', 'dog']
        #labels =indexer.search_by_query(search_query)
        #print()

if __name__ == "__main__":
    main()
