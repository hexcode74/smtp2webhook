#!/usr/bin/env python3
import smtpd
import asyncore
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import email
import configparser


######## config ##############
CONFIGPATH = '/etc/smtp2webhook/smtp2webhook.conf'
DEFAULTCONFIG = {
   'webhook_url': 'https://hooks.slack.com/services/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',
   'smtpd_port': 25
}

config = configparser.ConfigParser()
config.read(CONFIGPATH)

# get webhook url
webhook_url = config.get('DEFAULT', 'webhook_url')
smtpd_port = config.get('DEFAULT', 'smtpd_port')

##############################
headers = {'content-type': 'application/json'}

class SMTPServer(smtpd.SMTPServer):
	"""smtp to webhook server"""
	def __init__(*args, **kwargs):
		print('Running smtp to webhook on port %s' % (smtpd_port))
		smtpd.SMTPServer.__init__(*args, **kwargs)
	def process_message(self, peer, mailfrom, rcpttos, data):
		b = email.message_from_string(data)
		fr = b['from']
		to = b['to']
		subject = b['subject']
		body = ''
		if b.is_multipart():
			for part in b.walk():
				ctype = part.get_content_type()
				cdispo = str(part.get('Content-Disposition'))
				# skip any text/plain (txt) attachments
				if ctype == 'text/plain' and 'attachment' not in cdispo:
					body = part.get_payload(decode=True)  # decode
					break
		# not multipart - i.e. plain text, no attachments, keeping fingers crossed
		else:
			body = b.get_payload(decode=True)

		message = "From: " + fr + "\n" + "To: " + to + "\n" + "Subject: " + subject + "\n" + body
		# for debugging
		# print(message)
		try:
			values = {'text': message}
			req = Request(webhook_url, data=json.dumps(values), headers=headers)
			response = urlopen(req)

		except HTTPError as e:
			print(response.status)
			print(e)
			pass
		except URLError as e:
			print("The URL does not exist")
			print(e)
		
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
