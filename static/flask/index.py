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
from requests import get, post
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
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from flask_cors import CORS, cross_origin
from wtforms import StringField, TextAreaField, BooleanField, MultipleFileField, SubmitField, FileField
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
Bootstrap(app)
cors = CORS(app)

class ToDoForm(FlaskForm):
    description = StringField('description', validators=[])
    body = TextAreaField('body', validators=[])
    files = MultipleFileField('files', validators=[])
    # filenames = MultipleFileField('Media', validators=[FileRequired()])
    completed = BooleanField('completed', default=False,)
    submit = SubmitField('submit')

class UploadForm(FlaskForm):
    file = FileField('file', )
    files = MultipleFileField('files', )
    submit = SubmitField('submit')

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

@app.route('/home', methods=['GET', 'POST'])
@cross_origin()
def index():
    app.logger.debug(f"rendering home")
    todos = get(f"{API_URL}/todos")
    app.logger.debug(f"available todos {todos.json()}")
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
        app.logger.debug(f"user input {body}")

        # save file to local storage
        # TODO: accept multiple files
        # file = body['file']
        # filename = secure_filename(file.filename)
        # file.save(path.join(assets_dir, filename))
        # body['file'] = path.join(assets_dir, filename)
        # app.logger.debug(f"resolved body {body}")
        # create ToDo
        result = post(
            f"{API_URL}/todos",
            data=dumps(body),
            headers={
                'Content-Type': 'application/json'
            }
        )
        if 'id' in result.json():
            app.logger.debug(f"found ID in result")
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


@app.route('/delete', methods=['DELETE'])
@cross_origin()
def delete():
    app.logger.debug(f"rendering delete")
    return jsonify({'foo': 'bar'})

@app.route('/update', methods=['PUT'])
@cross_origin()
def update():
    return jsonify({'foo': 'bar'})
