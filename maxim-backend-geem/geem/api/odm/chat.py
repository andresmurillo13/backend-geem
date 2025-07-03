from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID


class CreateChatODM(Schema):

    message = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    created = fields.DateTime(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user_chat = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    task = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    pqrs = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    status = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    read = fields.DateTime(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )


class UseChatODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

