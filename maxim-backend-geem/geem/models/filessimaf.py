from tortoise import Model, fields


class ModelFilessimaf(Model):
    id = fields.IntField(pk=True)
    path_complete = fields.CharField(max_length=500)
    name = fields.CharField(max_length=200)
    created = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField('models.ModelUser')
    servicerequest = fields.ForeignKeyField('models.ModelServicerequest', null=True)

    class Meta:
        table = 'filessimaf'
