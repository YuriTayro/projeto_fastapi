from dataclasses import asdict

from sqlalchemy import select

from projeto_fastapi.models import User


# A função agora recebe 'mock_db_time', que seria uma fixture
# baseada no código que você me mostrou.
def test_create_user(session, mock_db_time):
    # 1. Inicia o gerenciador de contexto.
    # A partir daqui, o "ouvinte" de evento do
    # SQLAlchemy está ATIVO.
    # O valor do tempo é capturado na variável 'time'.
    with mock_db_time(model=User) as time:
        new_user = User(
            username='yuri', password='1234', email='teste@teste.com'
        )

        # 2. O usuário é adicionado à sessão...
        session.add(new_user)
        # 3. ...e salvo no banco.
        # É AQUI que o evento 'before_insert' dispara.
        session.commit()

        # 4. O usuário é recuperado do banco para verificação.
        user = session.scalar(select(User).where(User.username == 'yuri'))

        # 5. A asserção agora compara o objeto inteiro,
        # incluindo o 'created_at',
        # que deve ser igual ao tempo fixo capturado.
        assert asdict(user) == {
            'id': 1,
            'username': 'yuri',
            'password': '1234',
            'email': 'teste@teste.com',
            'created_at': time,
        }
