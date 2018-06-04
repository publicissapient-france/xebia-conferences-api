FROM python:3.6.4-alpine
LABEL Maintainer Alexis Horgix Chotad <alexis.horgix.chotard AT gmail.com>

RUN apk add --update git && rm -rf /var/cache/apk/*

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app

CMD ["gunicorn", "-w 3", "-b :80", "--chdir=/app/src", "server:app"]
