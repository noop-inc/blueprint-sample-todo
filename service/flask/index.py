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
from s3 import get_object, upload_object, delete_object, list_objects, list_key_objects
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
    if 'data' in data:
        filename = os.path.join('/tmp', data['filename'])
        img_data = data['data']
        # write the image data to a file on the service FS
        with open(os.path.join('/tmp', data['filename']), 'wb') as f:
            # decode the base64 string
            f.write(base64.b64decode(img_data))

        result = upload_object(f"{data['id']}/{data['filename']}", filename)
        app.logger.debug(f"{result}")

        return jsonify({
            'local': os.path.join('/tmp', data['filename']),
            'key': f"{data['id']}/{data['filename']}"
        })
    return jsonify(data)

@app.route('/api/images', methods=['GET'])
@cross_origin()
def images_list():
    results = []
    args = request.args
    if 'local' in args and bool(args['local']):
        results = [i for i in os.listdir('/tmp/') if i.endswith('.jpg')]
        # return jsonify(results)
    if 'remote' in args and bool(args['remote']):
        results = list_objects()
    return jsonify(results)

@app.route('/api/images/<image_id>', methods=['GET'])
@cross_origin()
def images_download(image_id):
    args = request.args
    result = {
        'message': '0 images associated with this todo'
    }
    images = list_key_objects(image_id)
    app.logger.debug(f"found {len(images)} files under key {image_id}")
    if len(images) == 0:
        return jsonify(result)

    if len(images) > 0 and 'filename' not in args:
        image = images[0] #
        app.logger.debug(f"using first image in list {image}")
        data = get_object(f"{image}")
        return data

    if len(images) > 0 and 'filename' in args:
        image = None
        for image_key in images:
            if args['filename'] in image_key:
                image = image_key
        data = get_object(f"{image}")
        return data

    return jsonify(result)
