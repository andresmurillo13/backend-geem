from tortoise import Model, fields


class ModelLogUser(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.ModelUser')
    company = fields.ForeignKeyField('models.ModelCompanies')
    controller = fields.CharField(max_length=150)
    event = fields.CharField(max_length=300)
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'logs_user'