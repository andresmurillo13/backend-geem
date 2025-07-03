from tortoise import Model, fields


class ModelActions(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    code = fields.CharField(unique=True, max_length=10)
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'actions'