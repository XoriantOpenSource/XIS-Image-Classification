from pymongo import MongoClient


class DbOperationsHandler:
    def __init__(self, config_settings):

        self.config_settings = config_settings

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
        except:
            print("failed to connect to db")
            # log error for db connection here
            return False

    def check_db_connection_status(self):
        if not (self.db and self.images):
            return self.establish_db_connection()
        return True

    def check_existence_of_image_doc(self, image):
        return not self.images.find({'image_object_name': image['image_object_name'], 'labels': image['labels']})

    def insert_image(self, image):
        if image is None:
            return False
        op_status = self.check_db_connection_status()
        # doc_existence = self.check_existence_of_image_doc(image)
        try:
            if op_status:
                self.images.insert_one(image)
                print("image document inserted successfully")
                return True
            else:
                # print("failed to insert image document")
                return False
        except:
            print("failed to insert image document")
            # log exception here
            return False

    def search_by_labels(self, labels):
        if not labels:
            return False
        op_status = self.check_db_connection_status()
        try:
            if op_status:
                return [image_doc['image_object_name'] for image_doc in self.images.find({'labels': {'$in': labels}})]
            else:
                print("failed to search")
                return False
        except:
            # log exception here
            return False

