from tortoise import Model, fields


class ModelContractsGerencies(Model):
    id = fields.IntField(pk=True)
    contracts = fields.ForeignKeyField('models.ModelContracts')
    gerencies = fields.ForeignKeyField('models.ModelGerencies')
    costcenter = fields.ForeignKeyField('models.ModelCostcenter')
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'contractsgerencies'