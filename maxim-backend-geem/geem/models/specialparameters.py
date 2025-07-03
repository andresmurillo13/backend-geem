from tortoise import Model, fields


class ModelSpecialparameters(Model):
    id = fields.IntField(pk=True)
    card_closing = fields.IntField(default=0)
    card_response = fields.IntField(default=0)
    pqrs_closing = fields.IntField(default=0)
    pqrs_response = fields.IntField(default=0)
    pqrs_centralizer = fields.BooleanField(default=False, null=True)
    correspondence_centralizer = fields.BooleanField(default=False, null=True)
    consecutive = fields.IntField(default=0)
    user_card = fields.ForeignKeyField('models.ModelUser', related_name="user_card", null=True)
    user_pqrs = fields.ForeignKeyField('models.ModelUser', related_name="user_pqrs", null=True)

    class Meta:
        table = 'specialparameters'