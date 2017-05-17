FROM tiangolo/uwsgi-nginx:python3.5
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY supervisord.conf /etc/supervisor/conf.d/memcached.conf
COPY bashrc /root/.bashrc
COPY secrets.json /root/secrets.json
COPY requirements/exact.txt /app/requirements.txt
RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y git-core memcached \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 1000 agcs
RUN useradd -Ms /bin/false -u 1000 -g 1000 agcs
