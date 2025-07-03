from tortoise import Model, fields


class ModelVersion(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=150, unique=False)
    status = fields.IntField(default=2)
    version = fields.IntField(unique=True)
    company = fields.ForeignKeyField('models.ModelCompanies')

    class Meta:
        table = 'version'