from flask import Flask, request, make_response, jsonify, abort
import json
from AppConfig.AppConfigSettings import AppConfigSettings
from Mongodb_OpsHandler.DbOperationsHandler import DbOperationsHandler

app = Flask(__name__)


# api = Api(app)
#
#
# class Initilizer:
#     def __init__(self):
#         self.configManager = None
#         self.dbOpsManager = None
#         self.initializationSuccessful = False
#
#     def initialize(self):
#         self.configManager = AppConfigSettings()
#         if self.configManager.read_config_settings():
#             self.dbOpsManager =self.dbOpsManager(self.configManager)
#             self.initializationSuccessful = True
#         else:
#             self.initializationSuccessful = False
#
#
# class Category(Resource):
#     def __init__(self):
#         # self.initializer = Initilizer()
#         # if not self.initializer.initializationSuccessful:
#         #     self.initializer.initialize()
#         super(Category, self).__init__()
#     def get(self):
#         return make_response(jsonify(['animals','plants','buildings']))
#
#
# class Label(Resource):
#     def __init__(self):
#         # self.initializer = Initilizer()
#         # if not self.initializer.initializationSuccessful:
#         #     self.initializer.initialize()
#         super(Label, self).__init__()
#         self.requestParser = reqparse.RequestParser()
#         self.requestParser.add_argument('query',type='list',required=True,location='json')
#         super(Label, self).__init__()
#
#     def post(self):
#         #return make_response(jsonify({"message":" Label's post hit"}))
#         args = self.requestParser.parse_args()['query']
#         print(args)
#         if len(args) == 0 or args is None:
#             return make_response(jsonify({"result":"No images found"}))
#         else:
#             return make_response(jsonify({"message": " Label's post hit"}))
#
#
# api.add_resource(Category, "/xis/api/v1.0/category", endpoint='category')
# api.add_resource(Label, '/xis/api/v1.0/label', endpoint='label')


def init_api():
    global config_settings, dbOpsHandler
    config_settings = AppConfigSettings()
    if config_settings.read_config_settings():
        dbOpsHandler = DbOperationsHandler(config_settings)


@app.route("/xis/api/v1.0/label", methods=['POST'])
def get_categories():
    image_query = request.get_json()
    if image_query is None or len(image_query) == 0:
        return abort(400)
    search_query = image_query['query']
    result = dbOpsHandler.search_by_labels(search_query)
    jsonResponse = json.dumps(result)
    if len(result) == 0 or result is None:
        return make_response(jsonify({"status":"failure","result": "[]"})), 404
    else:
        return make_response(jsonify({"status":"success","result": jsonResponse})), 200

if __name__ == "__main__":
    init_api()
    app.run(debug=True)
