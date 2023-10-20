ARG PYTHON_VERSION=3.11
ARG BASE_IMAGE=tiangolo/uwsgi-nginx-flask:python${PYTHON_VERSION}

FROM ${BASE_IMAGE}
COPY requirements.txt /app/.
RUN pip install -r requirements.txt
COPY . /app
COPY override/nginx.conf /etc/nginx/nginx.conf
COPY override/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV FUNCTIONALMODELSERVICE_SETTINGS /app/functionalmodelservice/instance/docker_cfg.py