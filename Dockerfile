FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

COPY archiver ./archiver
COPY conversion ./conversion
COPY api ./api
COPY utils ./utils
COPY config.py cli.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]

