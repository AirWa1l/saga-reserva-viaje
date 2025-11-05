FROM python:3.9-slim

WORKDIR /app

COPY app.py .

RUN pip install flask
RUN pip install --no-cache-dir flask requests

EXPOSE 5001

CMD ["python", "app.py"]