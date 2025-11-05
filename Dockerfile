# 1. Usar una imagen base oficial de Python
# Se usa "slim" para mantener la imagen ligera
FROM python:3.10-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de dependencias
COPY requirements.txt .

# 4. Instalar las dependencias
# --no-cache-dir ahorra espacio
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo el código de la aplicación al contenedor
COPY . .

# 6. Exponer el puerto en el que correrá FastAPI
EXPOSE 8000

# 7. El comando para iniciar la aplicación cuando el contenedor se lance
# uvicorn correrá en 0.0.0.0 para ser accesible desde fuera del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]