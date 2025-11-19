import grpc
import sys

# Añadimos la ruta para encontrar los archivos generados
sys.path.append('./auth-service')

# Importamos los archivos generados (asegúrate de que existan en auth-service/)
import auth_pb2
import auth_pb2_grpc

def run():
    # Conectamos al puerto expuesto en docker-compose (50051)
    print("🔌 Conectando al Auth Service vía gRPC...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        
        # Pide un token al usuario
        token = input("Pegue un token JWT válido aquí: ")
        
        print("\n📨 Enviando petición gRPC 'VerifyToken'...")
        try:
            response = stub.VerifyToken(auth_pb2.VerifyTokenRequest(token=token))
            print(f"\n✅ Respuesta del Servidor:")
            print(f"   - Es válido: {response.valid}")
            print(f"   - Usuario: {response.username}")
            print(f"   - ID: {response.user_id}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    run()