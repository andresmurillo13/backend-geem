from tortoise import Model, fields


class ModelPieces(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=100)
    code = fields.CharField(max_length=20, unique=True)
    brand = fields.CharField(max_length=100, null=True)
    measure = fields.CharField(max_length=30, null=True)
    available = fields.BooleanField(default=True)

    class Meta:
        table = 'pieces'