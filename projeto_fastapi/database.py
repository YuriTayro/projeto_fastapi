from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from projeto_fastapi.settings import Settings

# cria o motor de conexao
engine = create_engine(Settings().DATABASE_URL)


# fornece conexões individuais para cada
# requisição, garantindo que elas sejam abertas
# e fechadas corretamente.
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
