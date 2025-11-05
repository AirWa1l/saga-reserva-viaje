FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install flask requests

EXPOSE 5005

CMD ["python", "app.py"]