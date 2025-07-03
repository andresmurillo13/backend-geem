from tortoise import Model, fields


class ModelApprovals(Model):
    id = fields.IntField(pk=True)
    abbreviation = fields.CharField(max_length=30)
    number = fields.IntField()
    create = fields.DatetimeField(auto_now=True)
    statussign = fields.CharField(max_length=10)
    eticadatauser = fields.CharField(max_length=150)
    user = fields.ForeignKeyField('models.ModelUser')

    class Meta:
        table = 'approvals'