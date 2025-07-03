from tortoise import Model, fields


class ModelUser(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    num_document = fields.CharField(max_length=10, unique=True)
    first_name = fields.CharField(max_length=150)
    last_name = fields.CharField(max_length=200)
    phone = fields.CharField(max_length=15, unique=True)
    token = fields.TextField(null=True)
    token_expired = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    updated = fields.DatetimeField(null=True)
    created = fields.DatetimeField(auto_now_add=True)
    company = fields.ForeignKeyField('models.ModelCompanies')
    available = fields.BooleanField(default=True)
    per_general = fields.IntField(default=0)
    per_cvtools = fields.IntField(default=0)
    per_geem = fields.IntField(default=0)
    per_gportals = fields.IntField(default=0)
    position = fields.ForeignKeyField('models.ModelPosition')
    locations = fields.ForeignKeyField('models.ModelLocations')
    address = fields.CharField(max_length=300, null=True)
    birth_date = fields.DateField(null=True)
    start_date = fields.DateField(null=True)
    end_date = fields.DateField(null=True)
    eticadatauser = fields.CharField(max_length=150, null=True)
    aprovstatus = fields.CharField(max_length=45, null=True)
    controller = fields.BooleanField(null=True, default=False)
    rules = fields.ManyToManyField('models.ModelRules')

    class Meta:
        table = 'users'
