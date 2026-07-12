# API de gestion du planning (remplace le CGI Web_Planning + l'écriture directe sur
# events.xml partagé par le bot, incompatibles avec des conteneurs séparés).
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py main.py

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
