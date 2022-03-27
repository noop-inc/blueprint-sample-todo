import base64
import os
import logging
from logging import DEBUG
from logging import StreamHandler
from logging import Formatter
from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request
from dynamodb import scan_table, get_item, put_item, delete_item, update_item
from s3 import get_object, upload_object, delete_object
app = Flask(__name__)
cors = CORS(app)

defaults = {
    "name": "backend",
    "purpose": "CRUD methods for ToDo example application"
}

# configure logging
logging.basicConfig(level=DEBUG)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(
    Formatter('%(asctime)s %(levelname)s: %(message) s'
              '[in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)


@app.route('/api/_health')
@cross_origin()
def home():
    return jsonify(**defaults)

# get all todos

@app.route('/api/todos', methods=['GET'])
@cross_origin()
def list():
    result = scan_table()
    return jsonify((result))

# create new todo

@app.route('/api/todos', methods=['POST'])
@cross_origin()
def create():
    # error = None
    params = request.json
    result = put_item(params)
    return jsonify(result)

# get todo

@app.route('/api/todos/<todo_id>', methods=['GET'])
@cross_origin()
def get(todo_id=None):
    if todo_id:
        todo_id = {"id": todo_id}
        result = get_item(todo_id)
        return jsonify(result)
    return jsonify({})

# update todo
@app.route('/api/todos/<todo_id>', methods=['PUT'])
@cross_origin()
def update(todo_id=None):
    if todo_id:
        params = {**request.json, "id": todo_id}
        result = update_item(params)
        return jsonify(result)
    return jsonify({})

# delete todo

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
@cross_origin()
def delete(todo_id):
    result = delete_item(todo_id)
    return jsonify(result)

# image related functions
@app.route('/api/images', methods=['POST'])
@cross_origin()
def image_create():
    data = request.json
    if 'file' in data:
        filename = os.path.join('/tmp', data['filename'])
        img_data = data['file']
        # write the image data to a file on the service FS
        with open(os.path.join('/tmp', data['filename']), 'wb') as f:
            # decode base64 string
            f.write(base64.b64decode(img_data))

        result = upload_object(f"{data['id']}/{data['filename']}", filename)
        app.logger.debug(f"{result}")

        return jsonify({'name': os.path.join('/tmp', data['filename'])})
    return jsonify(data)
