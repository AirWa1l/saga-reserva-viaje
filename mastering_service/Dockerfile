# Dockerfile
FROM python:3.11-slim

# Crear un directorio para la app
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app.py .

# Exponer puerto (por defecto 8000)
EXPOSE 5010

# Comando de ejecución
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
