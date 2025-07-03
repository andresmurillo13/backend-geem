from tortoise import Model, fields


class ModelChatevents(Model):
    id = fields.IntField(pk=True)
    taskevents = fields.ForeignKeyField('models.ModelTaskevents')
    user_eventtask = fields.ForeignKeyField('models.ModelUser', related_name="user_chat_eventtask")
    finding = fields.ForeignKeyField('models.ModelFindings')
    message = fields.CharField(max_length=500)
    status = fields.IntField()
    created = fields.DatetimeField(null=True, auto_now=True)
    read = fields.DatetimeField(null=True)

    class Meta:
        table = 'chatevents'