from pymongo import MongoClient

from AppConfig.ConfigSettings import ConfigSettings


class DbOperationsHandler:
    def __init__(self, configSettings):

        self.config_settings = configSettings

        # db specific details
        self.port = int(self.config_settings.mongo_port)
        self.host = self.config_settings.mongo_host
        self.db_name = 'Image_Labels'
        self.collection_name = 'Images_Collection'
        self.db = None
        self.images = None
        self.establish_db_connection()

    def establish_db_connection(self):
        try:
            client = MongoClient(host=self.host, port=self.port)
            self.db = client.get_database(name=self.db_name)
            self.images = self.db.get_collection(name=self.collection_name)
            print("established connection to db successfully")
            return True

        except Exception:
            print(" failed to connect to db")
            # log error for db connection here
            return False

    def check_db_connection_status(self):
        if self.db is None or self.images is None:
            return self.establish_db_connection()
        return True

    def check_existence_of_image_doc(self, image):
        res = self.images.find({'image_object_name': image['image_object_name'],
                                'labels': image['labels']})
        if res is not None:
            print("image metadata already exists")
        return False if res is not None else True

    def insert_image(self, image):
        if image is None:
            return False
        op_status = self.check_db_connection_status()
        # doc_existence = self.check_existence_of_image_doc(image)
        try:
            if op_status is True:
                self.images.insert_one(image)
                print("image document inserted successfully")
                return True
            else:
                # print("failed to insert image document")
                return False

        except Exception as ex:
            print("failed to insert image document")
            # log exception here
            return False

    def search_by_labels(self, labels):
        if labels is None or len(labels) == 0:
            return False
        op_status = self.check_db_connection_status()
        try:
            if op_status is True:
                search_result = []
                result_image_docs = self.images.find({'labels': {'$in': labels}})
                for image_doc in result_image_docs:
                    search_result.append(image_doc['image_object_name'])
                    # search_result.append(image_doc)
                return search_result
            else:
                print("failed to search")
                return False

        except Exception as ex:

            # log exception here
            return False


def main():
    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        dbOps = DbOperationsHandler(config_settings)
        # image_doc = {'image_object_name': 'images_obj6', 'labels': ['cheetah', 'wild animal']}
        # dbOps.insert_image(image=image_doc)
        # search_filter = ['cat', 'dog']
        # filtered_results = dbOps.search_by_labels(search_filter)
        # for filtered_result in filtered_results:
        #     print(filtered_result)


if __name__ == '__main__':
    main()
