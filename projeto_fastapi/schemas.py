# Especifica as condições para a criação de um usuario.
# Atua como um contrato, juntamente com o Models.

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str  # token que representa a sessão do usuário
    # e que contém informações sobre o usuário
    token_type: str  # é um tipo de autenticação que será incluído
    # no cabeçalho de autorização de cada solicitação. Em geral,
    # o token_type para JWT é "bearer".
