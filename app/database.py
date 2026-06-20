from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


class Database:
    """
    Mantém uma única conexão (cliente) com o MongoDB durante
    todo o ciclo de vida da aplicação.
    """
    client: AsyncIOMotorClient = None
    db = None


database = Database()


async def connect_to_mongo():
    """Abre a conexão com o MongoDB Atlas ao iniciar a aplicação."""
    database.client = AsyncIOMotorClient(settings.mongodb_uri)
    database.db = database.client[settings.database_name]
    print(f"✅ Conectado ao MongoDB — banco: {settings.database_name}")


async def close_mongo_connection():
    """Fecha a conexão com o MongoDB ao desligar a aplicação."""
    if database.client:
        database.client.close()
        print("🔌 Conexão com MongoDB encerrada")


def get_clientes_collection():
    """Retorna a coleção 'clientes' para ser usada nas rotas."""
    return database.db["clientes"]
