FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 80
COPY / ./
CMD  find . -name 'requirement*' -type f -exec pip3 install -r '{}' ';' ; ls -la ; uvicorn main:app --host 0.0.0.0 --port 80
