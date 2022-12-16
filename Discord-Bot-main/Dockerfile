FROM python:3.8-alpine
WORKDIR /app
COPY /Bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY /Bot/ ./
CMD  find . -name 'requirement*' -type f -exec pip3 install -r '{}' ';' ; ls -la ; python -u UR-Bot.py
