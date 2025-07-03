from tortoise import Model, fields


class ModelTimeline(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now=True, null=False)
    docversion = fields.ForeignKeyField('models.ModelDocversion')
    aplication = fields.ForeignKeyField('models.ModelAplication')
    status = fields.BooleanField(default=True)
    avalilable = fields.BooleanField(default=True)
    position = fields.IntField()
    docid = fields.IntField(null=True)

    class Meta:
        table = 'timeline'