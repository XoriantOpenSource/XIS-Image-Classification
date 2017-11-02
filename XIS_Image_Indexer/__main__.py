from AppConfig.ConfigSettings import ConfigSettings
from XIS_Image_Indexer.ImageIndexer.Image_Indexer import ImageIndexer
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--source_dir', help='Directory containing images to be indexed')
    parser.add_argument('-t', '--target_dir', help='Directory where images may be downloaded')
    args = parser.parse_args()
    print(args.source_dir, args.target_dir)
    config_settings = ConfigSettings()
    if not config_settings.read_config_settings():
        print("error occurred while reading config")
    config_settings.source_images_location = args.source_dir
    config_settings.download_location = args.target_dir
    image_indexer = ImageIndexer(config_settings)

    # if run in index mode
    image_indexer.index_images()

    # run in search mode
    # query = ['cat','dog']
    # image_indexer.search_by_query(query)
    # return
