from tortoise import Model, fields


class ModelVersionitems(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=150)
    status = fields.IntField(default=2)
    version = fields.ForeignKeyField('models.ModelVersion')
    company = fields.ForeignKeyField('models.ModelCompanies')
    level = fields.IntField()
    level2 = fields.IntField()
    audit = fields.BooleanField(default=True)

    class Meta:
        table = 'versionitems'