from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID


class CreateFileODM(Schema):
    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    opt = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    base64 = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED, 'invalid': MESSAGE_INVALID}
    )

    name_file = fields.Field(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED, 'invalid': MESSAGE_INVALID}
    )