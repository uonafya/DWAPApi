from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from datetime import datetime, timedelta
import re
import json
import os
from django.contrib.sites.models import Site
from notifications.models import EmailConfig
from datetime import datetime
import logging
logger = logging.getLogger('ditapi_logger')


class DQITSEmailBackend:
    def __init__(self, request, subject='Testing mails', body="Hi, there is a system generated test mail. Ignore if you are reading this!", to=["titusowuor30@gmail.com"], attachments=[]):
        self.request = request
        self.subject = subject
        self.body = body
        self.to = to
        self.attachments = attachments

    def send_email(self):
        try:
            logger.debug(self.request.META['HTTP_HOST'])
            domain = self.request.META['HTTP_HOST']
            protocol = 'https' if self.request.is_secure() else 'http'
            site_login_url = str(
                protocol+'://'+str(domain).replace(str(domain).split(':')[1], '3000'))+"/login"
            config = EmailConfig.objects.first()
            logger.debug(config)
            # print(imap_settings.email_id, imap_settings.email_password)
            backend = EmailBackend(host=config.email_host, port=config.email_port, username=config.support_reply_email,
                                   password=config.email_password, use_tls=config.use_tls, fail_silently=config.fail_silently)
            # replace &nbsp; with space
            message = re.sub(r'(?<!&nbsp;)&nbsp;', ' ', strip_tags(self.body))
            message = message+f"\nDITS Portal url {site_login_url}"
            if len(self.attachments) > 0:
                logger.debug('check attachments...')
                email = EmailMessage(
                    subject=self.subject, body=message, from_email=config.support_reply_email, to=self.to, connection=backend)
                logger.debug(email)
                for attch in self.attachments:
                    email.attach(attch.name, attch.read(),
                                 attch.content_type)
                email.send()
                logger.debug('Email sent successfully!')
            else:
                email = EmailMessage(
                    subject=self.subject, body=message, from_email=config.support_reply_email, to=self.to, connection=backend)
                email.send()
                logger.debug('Email sent successfully!')
        except Exception as e:
            logger.debug(e)
            logger.debug("Email send error:{}".format(e))
