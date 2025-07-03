from tortoise import Model, fields


class ModelFixedline(Model):
    id = fields.IntField(pk=True)
    type = fields.IntField()
    status = fields.BooleanField(default=True)
    desdription = fields.CharField(max_length=200, null=False)
    lineservices = fields.IntField()
    typeservice = fields.IntField()
    created = fields.DatetimeField(auto_now=True, null=False)
    aplication = fields.ForeignKeyField('models.ModelAplication')

    class Meta:
        table = 'fixedline'