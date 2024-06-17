FROM python:3.8-alpine
WORKDIR UR-BOT-PROJECT
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN apk update
RUN apk add git
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "UR-Bot.py"]
