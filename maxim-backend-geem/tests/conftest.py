import asyncio
import os

import nest_asyncio
from pytest import fixture
from starlette.testclient import TestClient

from geem import settings, run, app


@fixture(scope='session')
async def create_db():
    command = f'PGPASSFILE={settings.PG_PASS_FILE} psql -d postgres -U {settings.DB_USER} -h {settings.DB_HOST} ' \
              f'-f {os.path.dirname(__file__)}/db.sql'
    os.system(command)
    await run(generate_schemas=True)


@fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture()
def client():
    nest_asyncio.apply()
    with TestClient(app=app) as test_client:
        yield test_client
