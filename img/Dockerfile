FROM tiangolo/uwsgi-nginx:python3.5
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install -r requirements/exact.txt
RUN apt-get update && apt-get install -y memcached \
    && rm -rf /var/lib/apt/lists/*
