from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request
from dynamodb import scan_table, get_item, put_item, delete_item, update_item

app = Flask(__name__)
cors = CORS(app)

defaults = {
    "name": "backend",
    "purpose": "CRUD methods for ToDo example application"
}
@app.route('/')
@cross_origin()
def home():
    return jsonify(**defaults)

@app.route('/api/item', methods=['GET'])
@cross_origin()
def list():
    result = scan_table()
    return jsonify((result))

@app.route('/api/item', methods=['POST'])
@cross_origin()
def create():
    # error = None
    params = request.json
    print(params)
    result = put_item(params)
    return jsonify(result)

@app.route('/api/item/<item_id>', methods=['DELETE'])
@cross_origin()
def delete(item_id):
    result = delete_item(item_id)
    return jsonify(result)


@app.route('/api/item/<item_id>', methods=['GET'])
@cross_origin()
def get(item_id = None):
    if item_id:
        item_id = {
            "id": item_id
        }
        result = get_item(item_id)
        return jsonify(result)
    return jsonify({})

@app.route('/api/item/<item_id>', methods=['PUT'])
@cross_origin()
def update(item_id = None):
    if item_id:
        params = {
            **request.json,
            "id": item_id
        }
        result = update_item(params)
        return jsonify(result)
    return jsonify({})
