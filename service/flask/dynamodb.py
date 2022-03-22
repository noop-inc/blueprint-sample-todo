from os import environ as environment
import string
import secrets
# from datetime import datetime
import boto3

S3_ENDPOINT = environment.get('S3_ENDPOINT',
                              'http://s3bucket.resources.noop.desktop:9000')
AWS_REGION = environment.get('AWS_REGION', 'us-west-2')
DYNAMODB_ENDPOINT = environment.get(
    'DYNAMODB_ENDPOINT', 'http://dynamodbtable.resources.noop.desktop:8000')
DYNAMODB_TABLE = environment.get('DYNAMODB_TABLE', 'DynamoDBTable')

dynamodb = boto3.resource('dynamodb',
    endpoint_url=DYNAMODB_ENDPOINT,
    region_name=AWS_REGION
)

def randomid(length = 24):
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
def scan_table():
    """scan_table

    Returns:
        list: a list of items present in the configured DynamoDB table
    """
    table = dynamodb.Table(DYNAMODB_TABLE)
    try:
        response = table.scan()
        data = response.get('Items', [])
        return data
    except:
        print('A scanning error occurred')
def get_item(item_id):
    """get_item

    Args:
        item_id (str): the id of the item

    Returns:
        dict: a dictionary represenation of the dynamodb record
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.get_item(
            Key={
                **item_id
            }
        )
        item = response.get('Item', {})
        return item
    except:
        print(f"An error occurred getting item with id ${id}")
def put_item(item):
    """put_item

    Args:
        item (dict): a python dictionary representing JSON inputs

        - title - title of todo
        - description - description of todo
        - complete - status of todo

    Returns:
        dict: if successful, returns dict containing inserted attribs, if not, returns responses metadata
    """
    item = {
        **item,
        **randomid()
    }
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.update_item(
        Key={"id": item['id']},
        UpdateExpression=
        f"set title=:title, description=:description, complete=:complete",
        ExpressionAttributeValues={
            ':title': str(item.get('title', 'Example todo')),
            ':description': str(item.get('description',
                                         'example description')),
            ':complete': bool(item.get('complete', False))
        },
        ReturnValues="ALL_NEW")
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Attributes']
    else:
        return {**response['ResponseMetadata']}
def update_item(item):
    """update_item

    Args:
        item (dict): a dictionary with the properties to update, must include `id`

    Returns:
        dict: updated attributes or response metadata
    """
    item = {
        **item
    }
    table = dynamodb.Table(DYNAMODB_TABLE)
    defaults = get_item(
        {
            'id': item.get('id')
        }
    )
    print(defaults)
    response = table.update_item(
        Key={'id': item['id']},
        UpdateExpression=
        f"set title=:title, description=:description, complete=:complete",
        ExpressionAttributeValues={
            ':title':
            str(item.get('title', defaults['title'])),
            ':description':
            str(item.get('description', defaults['description'])),
            ':complete':
            bool(item.get('complete', defaults['complete']))
        },
        ReturnValues="ALL_NEW")
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Attributes']
    else:
        return {**response['ResponseMetadata']}
def delete_item(item_id):
    """delete_item

    Args:
        item_id (str): id of item to delete

    Returns:
        dict: response data
    """
    item = {
        'id': item_id
    }
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.delete_item(
        Key={
            **item
        }
    )
    return response