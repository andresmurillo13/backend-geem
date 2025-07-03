from pytest import fixture

from geem.controllers import Actions, Create
from geem.models import ModelCompanies


@fixture(autouse=True, scope='session')
async def create_user_admin(create_db):
    company = await ModelCompanies.create(name='MAXIM FISHING SAS', nit='900000000-1', type=1, is_Active=True)
    await Create(email='tech@gmail.com', password='0000', first_name='Tech', last_name='Maxim',
                 phone='3166782345', company=company).userAdd()
