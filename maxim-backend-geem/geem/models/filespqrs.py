from tortoise import Model, fields


class ModelFilespqrs(Model):
    id = fields.IntField(pk=True)
    path_complete = fields.CharField(max_length=500)
    name = fields.CharField(max_length=200)
    created = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser')
    pqrs = fields.ForeignKeyField('models.ModelPqrs', null=True)
    task = fields.ForeignKeyField('models.ModelTask', null=True)
    card = fields.ForeignKeyField('models.ModelCard', null=True)
    task_card = fields.ForeignKeyField('models.ModelTaskcard', null=True)

    class Meta:
        table = 'filespqrs'
