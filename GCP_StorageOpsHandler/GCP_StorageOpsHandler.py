from os import listdir
from os.path import isdir, join, isfile, basename, splitext

from google.cloud import storage


class GCPStorageCrud:
    def __init__(self, app_config_settings):
        self.bucket_name = app_config_settings.gstorage_bucket_name
        self.app_config_settings = app_config_settings
        self.project_id = app_config_settings.project_id

    def get_storage_client(self):
        if self.project_id:
            return storage.Client(project=self.project_id)
        else:
            return None

    def upload_image(self, file_path):
        client = self.get_storage_client()
        if client is None:
            print("unable to initialize storage client instance")
            return
        filename = basename(file_path)
        try:
            with open(file_path, 'rb') as image_file:
                image_file_content = image_file.read()
                bucket = client.get_bucket(self.bucket_name)
                blob = bucket.blob(filename)
                file_extension = splitext(filename)[1].replace(".", "")
                blob.upload_from_string(image_file_content, content_type=str.format('image/{}', file_extension))

                # make object public
                blob.make_public(client)
                # return blob.public_url
                return True

        except IOError as io_error:
            print(io_error)
            return False
        except FileNotFoundError as file_not_found_error:
            print(file_not_found_error)
            return False

    def read_directory(self, dir_path):
        if not isdir(dir_path):
            raise NotADirectoryError("given path is not a directory")

        # image_extensions = ["jpg", "bmp", "png", "gif"]
        image_extensions = list(self.app_config_settings.image_files_extensions)
        # get image file paths with match filter criteria
        image_files = [join(dir_path, image_file) for image_file in listdir(dir_path) if
                       isfile(join(dir_path, image_file)) and
                       any(image_file.endswith(ext) for ext in image_extensions)]
        return image_files

    def upload_images(self):
        if not (self.app_config_settings and self.app_config_settings.source_images_location):
            print("source directory location not specified in config")
            return
        image_file_paths = self.read_directory(self.app_config_settings.source_images_location)
        if not image_file_paths:
            print("source directory doesn't contains any image files")
            return

        return [self.upload_image(image_file_path) for image_file_path in image_file_paths]

    def download_image(self, object_name):
        client = self.get_storage_client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(object_name)
        if blob:
            blob.download_to_filename(join(self.app_config_settings.download_location, object_name))
            print("{} downloaded successfully ".format(object_name))



