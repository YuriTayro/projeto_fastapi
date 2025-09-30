from http import HTTPStatus

from projeto_fastapi.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    user = UserPublic(**response.json())
    assert user.username == 'bob'
    assert user.email == 'bob@example.com'
    assert user.id == 2


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'new_email@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'new_user',
            'email': user.email,
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_delete_user__exercicio(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/users/{user.id}', headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_not_found__exercicio(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete('/users/666', headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Teste',
                'email': 'teste@test.com',
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Teste',
        'email': 'teste@test.com',
    }


def test_read_user_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK

    user = UserPublic(**response.json())
    assert user.username == 'bob'
    assert user.email == 'bob@example.com'
    assert user.id == 1


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_username_already_exists(client, user):
    other_user = client.post(
        '/users/',
        json={
            'username': 'other_user',
            'email': 'other@mail.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': other_user.json()['username'],
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert response.json()['token_type'] == 'bearer'


def test_get_token_invalid_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': 'wrong-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_get_token_invalid_username(client, user):
    response = client.post(
        '/token',
        data={'username': 'wrong-user', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}
