from tortoise import Model, fields


class ModelEnlistments(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True)
    modified = fields.DatetimeField(null=True)
    status = fields.IntField(defaul=1)
    servicerequest = fields.ForeignKeyField('models.ModelServicerequest')
    user = fields.ForeignKeyField('models.ModelUser')
    useralist = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_alist")
    toolsalist = fields.ForeignKeyField('models.ModelTools', null=True, related_name="tool_alist")
    is_work = fields.BooleanField(default=False)
    block = fields.BooleanField(null=True)

    class Meta:
        table = 'enlistments'