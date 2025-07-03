from tortoise import Model, fields


class ModelTaskevents(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=500, null=False)
    description_close = fields.CharField(max_length=500, null=True)
    description_evidence = fields.CharField(max_length=500, null=True)
    effectiv = fields.CharField(max_length=500, null=True)
    status = fields.IntField(null=False)
    created = fields.DatetimeField(auto_now=True, null=False)
    closed = fields.DatetimeField(null=True)
    updated = fields.DatetimeField(null=True)
    created_e = fields.DateField(null=False)
    closed_e = fields.DateField(null=True)
    user = fields.ForeignKeyField('models.ModelUser', related_name="user_resp_taskevents")
    finding = fields.ForeignKeyField('models.ModelFindings', related_name="finding")
    area = fields.ForeignKeyField('models.ModelAreas', related_name="area_taskevents")
    actiontask = fields.ForeignKeyField('models.ModelActiontask', related_name="action_task")


    class Meta:
        table = 'taskevents'