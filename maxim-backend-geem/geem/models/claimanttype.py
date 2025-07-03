from tortoise import Model, fields


class ModelClaimantType(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=200)
    status = fields.BooleanField(default=True)

    class Meta:
        table = 'claimanttype'