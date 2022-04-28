# FROM: base image
FROM ubuntu:20.04

MAINTAINER "jinduk@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    mkdir /usr/local/smtp2webhook && \
    mkdir /etc/smtp2webhook
COPY smtp2webhook.py /usr/local/smtp2webhook
COPY smtp2webhook.conf /etc/smtp2webhook

WORKDIR /usr/local/smtp2webhook

#RUN pip3 install -r requirements.txt

EXPOSE 25

# ENTRYPOINT: 컨테이너 시작 시 기본으로 실행되는 명령어 
ENTRYPOINT [ "python3" ]

# CMD: 컨테이너 시작 시 실행되는 명령어로 위 ENTRYPOINT 명령어 뒤 인자로 실행하게 된다. 
CMD [ "smtp2webhook.py" ]
