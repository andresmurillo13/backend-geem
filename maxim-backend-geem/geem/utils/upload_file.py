import base64
import os
from typing import Union, AnyStr
from uuid import uuid4

import boto3

NAME_BUCKET = 'gf5b-478b-8af8-l248f68cc8ea-upload-maximfishing.solutions'
s3 = boto3.resource('s3')


def generate_name(name_file):
    name_file = name_file.replace(' ', '_')
    return f'{uuid4().hex}/{name_file}'


def upload_file(data) -> Union[AnyStr, None]:
    try:
        name = generate_name(data.get("name_file"))
        document = open(data.get('name_file'), 'wb')
        document_64_encode = data.get('base64').split(';base64,')[1]
        document_64_decode = base64.decodestring(document_64_encode.encode('utf-8'))
        document.write(document_64_decode)
        s3.meta.client.upload_file(data.get('name_file'), NAME_BUCKET, name)
        object_acl = s3.ObjectAcl(NAME_BUCKET, name)
        object_acl.put(ACL='public-read')
        os.remove(data.get('name_file'))
        return f'https://s3.amazonaws.com/{NAME_BUCKET}/{name}'
    except Exception as error:
        return None


def delete_file(url: str):
    try:
        url = url.replace(f'https://s3.amazonaws.com/{NAME_BUCKET}/', '')
        client = boto3.client('s3')
        client.delete_object(
            Bucket=NAME_BUCKET,
            Key=url
        )
        return True
    except Exception as error:
        return None
