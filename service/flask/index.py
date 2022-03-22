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
