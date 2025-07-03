import asyncio

import nest_asyncio
from meliodas.model import client as client_db
from meliodas.settings import DB_NAME
from pytest import fixture
from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette.testclient import TestClient

from security.decorators.secure import secure
from security.utils import ReasonEnum

app = Starlette()


@app.route(path='/many-requests', methods=['GET'])
@secure(reason=ReasonEnum.many_requests.value)
async def many_requests(request):
    return UJSONResponse({'ok': True})


@app.route(path='/brute-force', methods=['GET'])
@secure(reason=ReasonEnum.brute_force.value)
async def brute_force(request):
    return UJSONResponse({'ok': True})


@fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture(autouse=True, scope='function')
async def drop_test_database():
    await client_db.drop_database(DB_NAME)
    yield


@fixture()
def client():
    nest_asyncio.apply()
    with TestClient(app=app) as test_client:
        yield test_client
