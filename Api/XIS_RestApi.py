from flask import Flask, request, make_response, jsonify, abort
import json
from AppConfig.ConfigSettings import ConfigSettings
from Mongodb_OpsHandler.DbOperationsHandler import DbOperationsHandler


app = Flask(__name__)


def init_api():
    global config_settings, dbOpsHandler
    config_settings = ConfigSettings()
    if config_settings.read_config_settings():
        dbOpsHandler = DbOperationsHandler(config_settings)


@app.route("/xis/api/v1.0/label", methods=['POST'])
def get_categories():
    image_query = request.get_json()
    if image_query is None or len(image_query) == 0:
        return abort(400)
    search_query = image_query['query']
    image_object_names = dbOpsHandler.search_by_labels(search_query)

    if len(image_object_names) == 0 or image_object_names is None:
        return make_response(jsonify({"status": "failure", "result": "[]"})), 404
    else:
        jsonResponse = json.dumps(image_object_names)
        return make_response(jsonify({"status":"success","result": jsonResponse})), 200

    # below logic
    # if len(image_object_names) == 0 or image_object_names is None:
    #     return make_response(jsonify({"status": "failure", "result": "[]"})), 404
    # else:
    #     encoded_images_list = [imageEncoderDecoder.encode_image(image_object_name) for image_object_name in image_object_names]
    #     jsonResponse = json.dumps(encoded_images_list)
    #     return make_response(jsonify({"status":"success","result": jsonResponse})), 200

if __name__ == "__main__":
    init_api()
    app.run(debug=True)
