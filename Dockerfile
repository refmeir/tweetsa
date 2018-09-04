FROM python:3.6.4
RUN apt-get update && apt-get install -y supervisor && apt-get install -y python-pip && pip install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


EXPOSE 5000
EXPOSE 9092