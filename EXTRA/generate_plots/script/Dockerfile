FROM python:3.11

WORKDIR /app

# set environment variables - Stops generation of Pycache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src/ /app/src/

WORKDIR /app/src

CMD ["python", "main.py"]
