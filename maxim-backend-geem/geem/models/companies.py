from tortoise import Model, fields


class ModelCompanies(Model):
    id = fields.IntField(pk=True)
    nit = fields.CharField(max_length=12, unique=True)
    name = fields.CharField(max_length=200)
    is_active = fields.BooleanField(default=True)
    updated = fields.DatetimeField(null=True)
    active = fields.DatetimeField(null=True)
    created = fields.DatetimeField(auto_now_add=True)
    is_user = fields.BooleanField(default=True)
    is_provider = fields.BooleanField(default=False)
    is_owner = fields.BooleanField(default=False)

    class Meta:
        table = 'companies'