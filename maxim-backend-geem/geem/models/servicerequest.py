from tortoise import Model, fields


class ModelServicerequest(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    date_request = fields.DateField()
    date_init = fields.DateField(null=True)
    date_end = fields.DateField(null=True)
    created = fields.DatetimeField(auto_now=True)
    closed = fields.DatetimeField(null=True)
    status = fields.IntField(defaul=1)
    companies = fields.ForeignKeyField('models.ModelCompanies')
    lineservices = fields.ForeignKeyField('models.ModelLineservices')
    contractsgerencies = fields.ForeignKeyField('models.ModelContractsGerencies')
    user = fields.ForeignKeyField('models.ModelUser')
    userresp1 = fields.ForeignKeyField('models.ModelUser', related_name="user_resp1")
    userresp2 = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_resp2")
    userresp3 = fields.ForeignKeyField('models.ModelUser', null=True, related_name="user_resp3")

    class Meta:
        table = 'servicerequest'