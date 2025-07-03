from tortoise import Model, fields


class ModelActiontype(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'actiontype'