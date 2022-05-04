# FROM: base image
FROM ubuntu:20.04

MAINTAINER "jinduk@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    mkdir /usr/local/smtp2webhook && \
    mkdir /etc/smtp2webhook
COPY smtp2webhook.py /usr/local/smtp2webhook
COPY requirements.txt /usr/local/smtp2webhook
COPY smtp2webhook.conf /etc/smtp2webhook

WORKDIR /usr/local/smtp2webhook

RUN pip3 install -r requirements.txt

EXPOSE 25

ENTRYPOINT [ "python3" ]

CMD [ "smtp2webhook.py" ]
