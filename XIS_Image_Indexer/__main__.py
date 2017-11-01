from AppConfig.ConfigSettings import ConfigSettings
from XIS_Image_Indexer.ImageIndexer.Image_Indexer import ImageIndexer


if __name__ == '__main__':
    config_settings = ConfigSettings()
    if not config_settings.read_config_settings():
        print("error occurred while reading config")
    config_settings.source_images_location = input("Directory to pick images from => ")
    config_settings.download_location = input("Directory where images may be downloaded => ")
    image_indexer = ImageIndexer(config_settings)

    # if run in index mode
    image_indexer.index_images()

    # run in search mode
    # query = ['cat','dog']
    # image_indexer.search_by_query(query)
    # return

