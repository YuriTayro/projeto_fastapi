from http import HTTPStatus

from fastapi import FastAPI

from projeto_fastapi.routers import auth, users
from projeto_fastapi.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message, tags=['default']
)
def read_root():
    return {'message': 'Olá Mundo!'}
