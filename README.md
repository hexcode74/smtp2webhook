## SMTP2Webhook (email to webhook server)

### Introduction
smtp2webhook is a simple SMTP server that resends the incoming email to the configured webhook url as a basic http post request.

When the SMTP server receives the mail, it parses the mail subject and body,  and sends it to the desired webhook url (like Messenger Channel)

### Dependency 
- CentOS 7 or Ubuntu 20.04
- Python 3.8+

### Installation
#### systemd based 
```
mkdir -p /usr/local/smtp2webhook/
cp smtp2webhook.py /usr/local/smtp2webhook/smtp2webhook.py
mkdir -p /etc/smtp2webhook 
cp smtp2webhook.conf /etc/smtp2webhook/smtp2webhook.conf
cp smtp2webhook.service /etc/systemd/system/smtp2webhook.service
systemctl daemon-reload
systemctl enable smtp2webhook
```

#### docker based
```
docker build -t smtp2webhook:0.1 .
```

### Usage
#### systemd based
```
if systemd 
systemctl start smtp2webhook
systemctl stop smtp2webhook
systemctl status smtp2webhook
```

#### docker based
```
docker run --name mysmtp -d -p 25:25 smtp2webhook:0.1
```

#### Notes:
Designate the server running the above daemon as the SMTP server for like appliance products, etc.
Since it is not an actual mail server, you can specify any e-mail address

