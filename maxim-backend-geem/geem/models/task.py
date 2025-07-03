from tortoise import Model, fields


class ModelTask(Model):
    id = fields.IntField(pk=True)
    pqrs = fields.ForeignKeyField('models.ModelPqrs')
    user_resp = fields.ForeignKeyField('models.ModelUser', related_name="user_resp_task")
    description = fields.CharField(max_length=1000)
    status = fields.IntField()
    obs = fields.CharField(max_length=1000, null=True)
    created = fields.DatetimeField(null=True, auto_now=True)
    closed = fields.DatetimeField(null=True)
    datestart = fields.DateField()
    datelimit = fields.DateField()

    class Meta:
        table = 'task'