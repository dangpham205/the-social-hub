ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

RUN apt-get update
# RUN apt-get install -y vim

WORKDIR /app

COPY . .
COPY requirements.txt .

RUN pip3 install -r requirements.txt
# RUN apt-get install -y sqlite3 libsqlite3-dev
# cd /
# wget https://github.com/Supervisor/supervisor/archive/4.2.0.tar.gz
# tar -xzvf 4.2.0.tar.gz
# cd supervisor-4.2.0
# apt-get -y install python3-setuptools
# pip3 install .
# supervisord
# pkill -HUP gunicorn

COPY ./docker/supervisor/conf.d /etc/supervisor/conf.d
COPY ./docker/deb /debdir
RUN dpkg -i /debdir/*.deb
RUN #apt-get update --fix-missing && apt-get install -y supervisor --fix-missing
RUN mkdir -p /var/log/supervisor
# CMD service supervisor start

#COPY . .

#RUN groupadd -g 1000 app_group
#
#RUN useradd -g app_group --uid 1000 zet
#
#RUN chown -R zet:app_group /app
#
#USER zet
#CMD ["gunicorn"]
ARG API_PORT
ENV API_PORT ${API_PORT}
EXPOSE ${API_PORT}
CMD uvicorn v1.api:app --host=0.0.0.0 --port ${API_PORT} --reload
# CMD ["uvicorn", "v1.api:app", "--host=0.0.0.0", "--port", ${API_PORT}, "--reload"]
