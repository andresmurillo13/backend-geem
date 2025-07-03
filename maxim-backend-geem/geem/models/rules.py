from tortoise import Model, fields


class ModelRules(Model):
    id = fields.IntField(pk=True)
    abbreviation = fields.CharField(max_length=30)
    description = fields.CharField(max_length=150)
    status = fields.BooleanField(default=True)
    statuslast = fields.CharField(max_length=10)
    statussign = fields.CharField(max_length=10)
    numaprov = fields.IntField()

    class Meta:
        table = 'rules'