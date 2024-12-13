from flask import jsonify
from notelab.app.app import api, app

@app.route('/swagger.json')
def swagger_json():
    return jsonify(api.__schema__)