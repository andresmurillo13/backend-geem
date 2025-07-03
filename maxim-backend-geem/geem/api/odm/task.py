from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID


class CreateTaskODM(Schema):
    description = fields.Str(
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

    obs = fields.Str(
        required=False,
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

    datestart = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    closed = fields.DateTime(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    datelimit = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    score = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    obs_final = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user_resp = fields.Int(
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

class UseTaskODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class DateTaskODM(Schema):

    date = fields.Date(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class UserTaskODM(Schema):

    user = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class UpdateObsODM(Schema):

    obs = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class DeliverObsODM(Schema):

    obs = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )
