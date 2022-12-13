FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update
RUN apk add git
COPY /Bot/requirements.txt bot/requirements.txt
RUN pip3 install -r bot/requirements.txt
COPY /Bot/ ./bot/
CMD ["python3", "bot/UR-Bot.py"]
