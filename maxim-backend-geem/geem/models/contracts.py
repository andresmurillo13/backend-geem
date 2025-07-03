from tortoise import Model, fields


class ModelContracts(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    code = fields.CharField(max_length=50)
    status = fields.BooleanField(default=True)
    companies = fields.ForeignKeyField('models.ModelCompanies')

    class Meta:
        table = 'contracts'