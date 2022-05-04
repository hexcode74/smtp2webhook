#!/usr/bin/env python3
import smtpd
import asyncore
import json
import requests
import email
import configparser


######## config ##############
CONFIGPATH = '/etc/smtp2webhook/smtp2webhook.conf'
# CONFIGPATH = './smtp2webhook.conf'
DEFAULTCONFIG = {
   'webhook_url': 'https://hooks.slack.com/services/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',
   'smtpd_port': 25
}

config = configparser.ConfigParser()
config.read(CONFIGPATH)

# get webhook url and smtpd port in CONFIGPATH file, if not exists set DEFALUTCONFIG
try:
	webhook_url = config.get('DEFAULT', 'webhook_url')
except configparser.NoOptionError:
	webhook_url = DEFAULTCONFIG['webhook_url']

try:
	smtpd_port = config.get('DEFAULT', 'smtpd_port')
except configparser.NoOptionError:
	smtpd_port = DEFAULTCONFIG['smtpd_port']

##############################
headers = {'content-type': 'application/json'}
class SMTPServer(smtpd.SMTPServer):
	"""smtp to webhook server"""
	def __init__(self, *args, **kwargs):
		print('Running smtp to webhook on port %s' % smtpd_port)
		smtpd.SMTPServer.__init__(self, *args, **kwargs)

	def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
		b = email.message_from_string(data.decode())
		fr = str(b['from'])
		to = str(b['to'])
		subject = str(b['subject'])
		body = ''
		if b.is_multipart():
			for part in b.walk():
				ctype = part.get_content_type()
				cdispo = str(part.get('Content-Disposition'))
				# skip any text/plain (txt) attachments
				if ctype == 'text/plain' and 'attachment' not in cdispo:
					body = part.get_payload()
					break
		# not multipart - i.e. plain text, no attachments, keeping fingers crossed
		else:
			body = b.get_payload()

		message = "From: " + fr + "\n" + "To: " + to + "\n" + "Subject: " + subject + "\n" + body
		# for debugging
		# print(message)
		try:
			values = {'text': message}
			requests.post(webhook_url, data=json.dumps(values), headers=headers)

		except Exception as e:
			print(e)
			pass
	pass
if __name__ == "__main__":
	smtp_server = SMTPServer(('0.0.0.0', int(smtpd_port)), None)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		smtp_server.close() 

