from tortoise import Model, fields


class ModelGerencies(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    name = fields.CharField(max_length=50)
    status = fields.BooleanField(default=True)
    companies = fields.ForeignKeyField('models.ModelCompanies')

    class Meta:
        table = 'gerencies'