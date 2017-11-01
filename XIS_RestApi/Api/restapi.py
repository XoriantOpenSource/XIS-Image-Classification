import json
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify, abort

from AppConfig.ConfigSettings import ConfigSettings
from Mongodb_OpsHandler.DbOperationsHandler import DbOperationsHandler

app, config_setting, db_ops_handler = Flask(__name__), None, None
CORS(app)


def init_api():
    global config_setting, db_ops_handler
    if config_setting and db_ops_handler:
        return
    config_setting = ConfigSettings()
    if config_setting.read_config_settings():
        db_ops_handler = DbOperationsHandler(config_setting)


init_api()


@app.route("/xis/api/v1.0/label", methods=['POST'])
def get_categories():
    image_query = request.get_json()
    if not image_query:
        return abort(400)
    search_query = image_query['query']
    image_object_names = db_ops_handler.search_by_labels(search_query)
    if not image_object_names:
        return make_response(jsonify({"status": "failure", "result": "[]"})), 404
    else:
        json_response = json.dumps(image_object_names)
        return make_response(jsonify({"status": "success", "result": json_response})), 200

        # below logic is for sending image as base64 encoded string
        # if len(image_object_names) == 0 or image_object_names is None:
        #     return make_response(jsonify({"status": "failure", "result": "[]"})), 404
        # else:
        #     encoded_images_list =
        # [imageEncoderDecoder.encode_image(image_object_name) for image_object_name in image_object_names]
        #     json_response = json.dumps(encoded_images_list)
        #     return make_response(jsonify({"status":"success","result": json_response})), 200


if __name__ == "__main__":
    init_api()
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
