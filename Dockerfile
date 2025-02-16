FROM python:3.11

COPY . /app

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential libcogl-pango-dev ffmpeg

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt

VOLUME ["/app"]

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
