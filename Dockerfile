FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests build-essential libpq-dev python3-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 8000


ENTRYPOINT ["python3.9","main.py"]
