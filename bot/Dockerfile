FROM python:3.11
WORKDIR /app
COPY /requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./ ./
CMD  find . -name 'requirement*' -type f -exec pip3 install -r '{}' ';' ; ls -la ; python -u UR-Bot.py
