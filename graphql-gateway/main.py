import strawberry
from typing import List, Optional
import httpx
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# --- 1. Definición de Tipos (Schema) ---

# Definimos cómo se ve un Usuario en GraphQL
# (Debe coincidir con lo que devuelve tu Auth Service)
@strawberry.type
class User:
    id: str
    username: str
    email: str
    full_name: Optional[str] = None

# Definimos un tipo "Pedido" (Simulado para el ejemplo)
@strawberry.type
class Order:
    id: int
    product_name: str
    price: float

# --- 2. Resolvers (La lógica que busca los datos) ---

async def get_users_from_api() -> List[User]:
    """
    Llama al Auth Service vía HTTP para obtener los usuarios reales.
    """
    url = "http://auth-service:8000/users" # Nombre del servicio en Docker
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            # Convertimos el JSON a objetos User de Strawberry
            return [
                User(
                    id=u["_id"], # Ojo: Auth Service devuelve "_id", aquí lo mapeamos a "id"
                    username=u["username"],
                    email=u["email"],
                    full_name=u.get("full_name")
                ) for u in data
            ]
    except Exception as e:
        print(f"Error conectando a Auth Service: {e}")
        return []

def get_orders_by_user(user_id: str) -> List[Order]:
    """
    Simula buscar pedidos de un usuario.
    En la vida real, aquí harías: await client.get(f"http://order-service/orders/{user_id}")
    """
    # Simulamos que todos tienen un pedido de prueba
    return [
        Order(id=101, product_name="Laptop Gamer", price=1500.00),
        Order(id=102, product_name="Mouse", price=25.50)
    ]

# --- 3. Query Principal ---

@strawberry.type
class Query:
    
    # Campo: users -> Devuelve una lista de usuarios
    @strawberry.field
    async def users(self) -> List[User]:
        return await get_users_from_api()

    # Campo: user_with_orders -> Ejemplo de consulta combinada (Req. 2.3)
    # Devuelve un usuario y sus pedidos "inyectados" al vuelo
    @strawberry.field
    async def my_orders(self, user_id: str) -> List[Order]:
        return get_orders_by_user(user_id)

# --- 4. Configuración de la App ---

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="GraphQL Gateway")
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def health_check():
    return {"status": "ok"}