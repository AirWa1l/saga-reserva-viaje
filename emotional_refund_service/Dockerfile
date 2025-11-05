FROM python:3.9-slim

WORKDIR /app

COPY app.py .

# Instala Flask y Requests directamente
RUN pip install --no-cache-dir flask requests

# Expón el puerto correcto (5004 según tu app.py)
EXPOSE 5004

CMD ["python", "app.py"]
