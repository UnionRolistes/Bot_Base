FROM python:3.8-alpine
WORKDIR /app
COPY /Bot/requirements.txt bot/requirements.txt
RUN pip3 install -r bot/requirements.txt
COPY /Bot/ ./bot/
CMD  find . -name 'requirement*' -type f -exec pip3 install -r '{}' ';' && python3 bot/UR-Bot.py
