import requests
import secrets
# import string
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import url_for
from flask_bootstrap import Bootstrap

from os import environ as environment
from flask_wtf import FlaskForm
from flask_cors import CORS, cross_origin
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, regexp


from flask import render_template

API_URL = environment.get('API_URL', 'https://todo.local.noop.app/api')
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
Bootstrap(app)
cors = CORS(app)

class ToDoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    file = FileField('Media', validators=[regexp(u'^[^/\\]\.jpg$')])
    completed = BooleanField('Completed', default=False,)
    submit = SubmitField('submit')

@app.route('/home', methods=['GET', 'POST'])
@cross_origin()
def index():
    todos = requests.get(f"{API_URL}/todos")
    form = ToDoForm()
    if form.validate_on_submit():
        body = {
            'description': form.description.data,
            'body': form.body.data,
            'file': form.file.data,
            'completed': form.completed.data
        }
        # print(body)

        result = requests.post(
            f"{API_URL}/item",
            json=body,
            headers={
                'Content-Type': 'application/json'
            }
        )
        todos = requests.get(f"{API_URL}/todos")

        # print(result.json())
        return redirect(url_for('index'))
        # return render_template('index.html', form=form, data=todos.json())

    return render_template('index.html', form=form, data=todos.json())

@app.route('/delete', methods=['DELETE'])
@cross_origin()
def delete():
    return jsonify({'foo': 'bar'})

@app.route('/update', methods=['PUT'])
@cross_origin()
def update():
    return jsonify({'foo': 'bar'})
