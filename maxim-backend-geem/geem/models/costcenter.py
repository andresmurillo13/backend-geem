from tortoise import Model, fields


class ModelCostcenter(Model):
    id = fields.IntField(pk=True)
    description = fields.CharField(max_length=200)
    cost_center = fields.CharField(max_length=50)
    status = fields.BooleanField(default=True)
    count_number = fields.CharField(max_length=50, null=True)

    class Meta:
        table = 'costcenter'