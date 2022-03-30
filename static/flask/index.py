from os import path
from os import environ as environment
from os.path import basename
from os.path import join as pathjoin
import logging
from logging import DEBUG
from logging import StreamHandler
from logging import Formatter
from json import dumps
import requests
from requests import get, post, put
import secrets
import mimetypes
from mimetypes import MimeTypes
import base64
from base64 import b64encode
# import string
from flask import request
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import flash
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_cors import CORS, cross_origin
from wtforms import StringField, TextAreaField, BooleanField, MultipleFileField, SubmitField, FileField
from flask_bootstrap import SwitchField
# from flask_uploads import configure_uploads, IMAGES, UploadSet
# from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, regexp


from flask import render_template

API_URL = environment.get('API_URL', 'https://todo.local.noop.app/api')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
assets_dir = pathjoin(
    path.dirname(app.instance_path), 'static', 'assets'
)
app.config['UPLOAD_FOLDER'] = assets_dir
# app.config['UPLOADED_IMAGES_DEST'] = 'static/assets'
# files = UploadSet('files', IMAGES)
# configure_uploads(app, files)
app.secret_key = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# configure logging
logging.basicConfig(level=DEBUG)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(
    Formatter(
        '%(asctime)s %(levelname)s: %(message) s'
        '[in %(pathname)s:%(lineno)d]'
    )
)
app.logger.addHandler(handler)
#app.logger.setLevel(DEBUG)
bootstrap = Bootstrap5(app)
cors = CORS(app)

class ToDoForm(FlaskForm):
    description = StringField(label='description', validators=[])
    body = TextAreaField(label='body', validators=[])
    files = MultipleFileField(label='files', validators=[])
    # filenames = MultipleFileField('Media', validators=[FileRequired()])
    completed = SwitchField(label='completed', default=False,)
    submit = SubmitField(label='submit')

class UploadForm(FlaskForm):
    file = FileField(label='file', )
    files = MultipleFileField(label='files', )
    submit = SubmitField(label='submit')

@app.route('/upload', methods=['GET', 'POST'])
@cross_origin()
def upload():
    app.logger.debug(f"rendering upload form")
    form = UploadForm()
    if form.validate_on_submit():
        # handle file
        uploaded_files = []
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(pathjoin(
            assets_dir,
            filename
        ))
        uploaded_files.append(filename)

        files = form.files.data
        for file in files:
            filename = secure_filename(file.filename)
            file.save(pathjoin(
                assets_dir,
                filename
            ))
            uploaded_files.append(filename)

        return f"uploaded {uploaded_files}"

        #app.logger.debug(f"forms files are < {form.files.data} >")
        #return f"Filename: {filename}"
    return render_template('upload.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():

    todos = get(f"{API_URL}/todos")
    form = ToDoForm()
    uploaded_files = []
    #file_form = UploadForm()
    if form.validate_on_submit():

        # handle list of files
        files = form.files.data
        for file in files:
            filename = secure_filename(file.filename)
            file.save(pathjoin(
                assets_dir,
                filename
            ))
            uploaded_files.append(filename)

        # handle s3 uploads

        # load form data
        body = {
            'description': form.description.data,
            'body': form.body.data,
            'files': uploaded_files,
            'completed': form.completed.data
        }
        app.logger.debug(f"sending parameters [  {body}  ]")
        result = post(
            f"{API_URL}/todos",
            data=dumps(body),
            headers={
                'Content-Type': 'application/json'
            }
        )
        if 'id' in result.json():
            for file in files:
                filename = secure_filename(file.filename)
                img_file = pathjoin(assets_dir, filename)
                with open(img_file, 'rb') as f:
                    mime = MimeTypes().guess_type(img_file)[0]
                    img_bytes = f.read()
                    img_enc = b64encode(img_bytes).decode('utf-8')
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'text/plain'
                    }
                    payload = {
                        **result.json(),
                        'mimetype': mime,
                        'filename': basename(img_file),
                        'data': img_enc
                    }
                    upload_result = post(
                        f"{API_URL}/images",
                        data=dumps(payload),
                        headers=headers
                    )
                    app.logger.debug(f"image publish results {upload_result.json()}")
        else:
            app.logger.debug(f"no id in result")


        app.logger.debug(f"create result {result.json()}")
        # app.logger.debug(f"create request: {result}")
        todos = requests.get(f"{API_URL}/todos")
        app.logger.debug(f"todos {todos.json()}")
        return redirect(url_for('index'))
    else:
        return render_template('index.html', form=form, data=todos.json())


@app.route('/<todo_id>', methods=['GET', 'POST'])
@cross_origin()
def details(todo_id):
    todos = get(f"{API_URL}/todos").json()
    form = ToDoForm()
    data = None
    for todo in todos:
        if todo['id'] == todo_id:
            data = todo
    if data is not None:
        form.description.default = todo['description']
        form.body.default = todo['body']
        form.completed.default = todo['completed']

        if form.validate_on_submit():
            description = form.description.data
            body = form.body.data
            files = form.files.data
            completed = form.completed.data

            body = {
                'description': description,
                'body': body,
                'files': [file.filename for file in files],
                'completed': completed
            }
            result = put(
                f"{API_URL}/todos/{todo_id}",
                data=dumps(body),
                headers={
                    'Content-Type': 'application/json'
                }
            ).json()
            # handle uploading new file to bucket key
            if 'id' in result:
                for file in files:
                    filename = secure_filename(file.filename)
                    img_file = pathjoin(assets_dir, filename)
                    with open(img_file, 'rb') as f:
                        mime = MimeTypes().guess_type(img_file)[0]
                        img_bytes = f.read()
                        img_enc = b64encode(img_bytes).decode('utf-8')
                        headers = {
                            'Content-Type': 'application/json',
                            'Accept': 'text/plain'
                        }
                        payload = {
                            **result, 'mimetype': mime,
                            'filename': basename(img_file),
                            'data': img_enc
                        }
                        upload_result = post(f"{API_URL}/images",
                                            data=dumps(payload),
                                            headers=headers).json()
                        app.logger.debug(f"image upload results {upload_result}")
            app.logger.debug(f"update result {result}")
            return redirect(url_for('index'))
        return render_template('todo.html', data=data, form=form)
    return redirect(url_for('index'))
