from tortoise import Model, fields


class ModelTaskcard(Model):
    id = fields.IntField(pk=True)
    card = fields.ForeignKeyField('models.ModelCard')
    user_resp = fields.ForeignKeyField('models.ModelUser', related_name="user_resp_task_card")
    description = fields.CharField(max_length=1000)
    status = fields.IntField()
    obs = fields.CharField(max_length=1000, null=True)
    created = fields.DatetimeField(null=True, auto_now=True)
    closed = fields.DatetimeField(null=True)
    datestart = fields.DateField()
    datelimit = fields.DateField()

    class Meta:
        table = 'taskcard'