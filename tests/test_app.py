from http import HTTPStatus


def test_root_deve_retornar_ok_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello world'}


def test_created_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'yuri',
            'email': 'teste@teste.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'yuri', 'email': 'teste@teste.com'}


def test_read_users(client):
    # Primeiro, cria um usuário para garantir que o
    # banco de dados não está vazio
    client.post(
        '/users/',
        json={
            'username': 'yuri',
            'email': 'teste@teste.com',
            'password': '1234',
        },
    )

    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': [{'username': 'yuri', 'email': 'teste@teste.com'}],
    }
