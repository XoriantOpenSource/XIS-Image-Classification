from os import listdir
from os.path import isdir, join, isfile, basename, splitext

from google.cloud import storage

from XIS_RestApi.AppConfig.ConfigSettings import ConfigSettings


class GCP_Storage_Crud:
    def __init__(self, appConfigSettings):
        self.bucket_name = appConfigSettings.gstorage_bucket_name
        self.appConfigSettings = appConfigSettings
        self.project_id = appConfigSettings.project_id

    def get_storage_client(self):
        if self.project_id is not None:
            return storage.Client(project=self.project_id)
        else:
            return None

    def upload_image(self, filepath):
        client = self.get_storage_client()
        if client is None:
            print("unable to initialize storage client instance")
            return
        filename = basename(filepath)
        try:
            with open(filepath, 'rb') as imagefile:
                imagefileContent = imagefile.read()
                bucket = client.get_bucket(self.bucket_name)
                blob = bucket.blob(filename)
                file_extension = splitext(filename)[1].replace(".", "")
                blob.upload_from_string(imagefileContent, content_type=str.format('image/{}', file_extension))

                # make object public
                blob.make_public(client)
                # return blob.public_url
                return True

        except IOError as ioerror:
            print(ioerror)
            return False
        except FileNotFoundError as fileNotfoundError:
            print(fileNotfoundError)
            return False

    def read_directory(self, dir_path):
        if not isdir(dir_path):
            raise NotADirectoryError("given path is not a directory")

        image_extensions = ["jpg", "bmp", "png", "gif"]

        # get image file paths with match filter criteria
        image_files = [join(dir_path, image_file) for image_file in listdir(dir_path) if
                       isfile(join(dir_path, image_file)) and
                       any(image_file.endswith(ext) for ext in image_extensions)]
        return image_files

    def upload_images(self):
        if self.appConfigSettings is None or self.appConfigSettings.source_images_location is None:
            print("source directory location not specified in config")
            return
        image_file_paths = self.read_directory(self.appConfigSettings.source_images_location)
        file_urls = []
        if image_file_paths is None or len(image_file_paths) == 0:
            print("source directory doesn't contains any image files")
            return

        for imagefilePath in image_file_paths:
            file_urls.append(self.upload_image(imagefilePath))
        return file_urls

    def download_image(self, object_name):
        client = self.get_storage_client()
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(object_name)
        if blob is not None:
            blob.download_to_filename(join(self.appConfigSettings.download_location, object_name))
            print("{} downloaded successfully ".format(object_name))


if __name__ == '__main__':

    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        crud = GCP_Storage_Crud()
        # crud.download_images()
        file_urls = crud.upload_images()
        print(file_urls)
    else:
        print("error reading config settings")
