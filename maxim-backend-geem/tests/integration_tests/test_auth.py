from pytest import mark

from geem.settings import MESSAGE_REQUIRED


@mark.asyncio
async def test_login_success(create_db, client):
    response = client.post('/auth/login', json={'email': 'tech@gmail.com', 'password': '0000'})
    assert response.json()['ok'] is True
    assert response.json()['token']
    assert response.json()['company'][0]
    assert response.json()['userid']


@mark.asyncio
async def test_login_invalid_password(create_db, client):
    response = client.post('/auth/login', json={'email': 'tech@gmail.com', 'password': '12345'})
    assert response.json()['ok'] is False
    assert not response.json().get('token')
    assert not response.json().get('company')
    assert not response.json().get('userid')


@mark.asyncio
async def test_login_invalid_user(create_db, client):
    response = client.post('/auth/login', json={'email': 'test@gmail.com', 'password': '00000'})
    assert response.json()['ok'] is False
    assert not response.json().get('token')
    assert not response.json().get('company')
    assert not response.json().get('userid')
    response = client.post('/auth/login', json={'email': '', 'password': ''})
    assert response.json()['ok'] is False
    assert response.json()['errors']['password'][0] == MESSAGE_REQUIRED
    assert response.json()['errors']['email'][0] == MESSAGE_REQUIRED


@mark.asyncio
async def test_login_verify_success(create_db, client):
    response = client.post('/auth/login', json={'email': 'tech@gmail.com', 'password': '0000'})
    token_user = response.json()['token']
    response = client.get('/auth/verify', headers={'authorization': f'Bearer {token_user}'})
    assert response.json()['ok'] is True


@mark.asyncio
async def test_login_verify_fail(create_db, client):
    response = client.get('/auth/verify', headers={'authorization': f'Bearer token_invalid'})
    assert response.json()['ok'] is False
    assert response.json()['errors'] == {}
    assert response.json()['message'] == 'Las credenciales de autenticación no se proveyeron.'
