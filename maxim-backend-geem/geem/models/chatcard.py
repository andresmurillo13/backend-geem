from tortoise import Model, fields


class ModelChatcard(Model):
    id = fields.IntField(pk=True)
    taskcard = fields.ForeignKeyField('models.ModelTaskcard')
    user_chatitem = fields.ForeignKeyField('models.ModelUser', related_name="user_chat_item")
    card = fields.ForeignKeyField('models.ModelCard')
    message = fields.CharField(max_length=500)
    status = fields.IntField()
    created = fields.DatetimeField(null=True, auto_now=True)
    read = fields.DatetimeField(null=True)

    class Meta:
        table = 'chatcard'