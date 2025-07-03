from tortoise import Model, fields


class ModelChat(Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField('models.ModelTask')
    user_chat = fields.ForeignKeyField('models.ModelUser', related_name="user_chat")
    pqrs = fields.ForeignKeyField('models.ModelPqrs')
    message = fields.CharField(max_length=500)
    status = fields.IntField()
    created = fields.DatetimeField(null=True, auto_now=True)
    read = fields.DatetimeField(null=True)

    class Meta:
        table = 'chat'