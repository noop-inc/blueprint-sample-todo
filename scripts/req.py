import requests
import base64
import mimetypes
import json
import string
import secrets
from os import environ as env
from os.path import basename
API_URL = env.get('API_URL', 'https://todo.local.noop.app/api')


def randomid(length: int = 24) -> dict:
    """randomid

    Args:
        length (int, optional): length. Defaults to 24.

    Returns:
        dict: a dictionary containing a generated `id` key
    """
    alphabet = string.ascii_letters + string.digits
    generated = ''.join(secrets.choice(alphabet) for i in range(length))
    #timestamp = datetime.isoformat(datetime.now())
    return {
        "id": generated,
        #"timestamp": timestamp
    }

img_file = f'static/flask/static/assets/placeholder.jpg'
with open(img_file, 'rb') as f:
    mime = mimetypes.MimeTypes().guess_type(img_file)[0]
    fbytes = f.read()
    fbase64 = base64.b64encode(fbytes) # .decode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
    }
    payload = {
        **randomid(),
        'mimetype': mime,
        'filename': basename(img_file),
        'data': fbase64.decode('utf-8'), #convert to string for serialization
    }
    result = requests.post(
        f"{API_URL}/images",
        data=json.dumps(payload),
        headers=headers

    )
    print(result.json())