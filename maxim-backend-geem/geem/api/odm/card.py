from marshmallow import Schema, fields

from geem.settings import MESSAGE_REQUIRED, MESSAGE_INVALID

class CreateCardODM(Schema):
    type = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    document = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    first_name = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    last_name = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    company = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    position = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    obs = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    action = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    close = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    site = fields.Str(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    user_obs = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    locations = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    simaf = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    companies = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    zone = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    items = fields.List(fields.Int(), required=True)

class UseCardODM(Schema):

    id = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class DateCardODM(Schema):

    created = fields.DateTime(
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

class RespCardODM(Schema):

    user = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    areas = fields.Int(
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

class GetCardUser(Schema):

    user = fields.Int(
        required=True,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    page = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    key = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    status = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class GetCardResp(Schema):

    user = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    page = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    key = fields.Str(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    type = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

    form = fields.Int(
        required=False,
        error_messages={
            'required': MESSAGE_REQUIRED,
            'invalid': MESSAGE_INVALID
        }
    )

class CloseCardODM(Schema):

    close = fields.Str(
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



