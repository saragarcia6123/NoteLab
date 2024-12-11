from flask import jsonify
from notelab.app.app import flask_api, app

@app.route('/swagger.json')
def swagger_json():
    return jsonify(flask_api.__schema__)