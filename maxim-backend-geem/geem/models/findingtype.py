from tortoise import Model, fields


class ModelFindingtype(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'findingtype'