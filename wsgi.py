from XIS_RestApi.Api.restapi import app, init_api

if __name__ == "__main__":
    init_api()
    app.run(host='0.0.0.0', debug=True, threaded=True)
