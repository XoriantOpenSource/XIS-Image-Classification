from AppConfig.ConfigSettings import ConfigSettings
from XIS_Image_Indexer.ImageIndexer.Image_Indexer import ImageIndexer


def main():
    config_settings = ConfigSettings()
    if not config_settings.read_config_settings():
        print("error occurred while reading config")
        return
    image_indexer = ImageIndexer(config_settings)

    # if run in index mode
    image_indexer.index_images()

    # run in search mode
    # query = ['cat','dog']
    # image_indexer.search_by_query(query)
    # return


if __name__ == "__main__":
    main()
