from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from projeto_fastapi.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

# provisorio
database = []


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    # O '**' vai descompactar o resultado de user.model_dump()
    # (q é um dicionário),
    # passando seus pares chave-valor como argumentos
    # para criar o novo objeto UserDB, adicionando o id
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'user': database}


@app.put(
    '/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}', response_model=Message, status_code=HTTPStatus.OK
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    database.pop(user_id - 1)
    return {'message': 'User deleted'}
