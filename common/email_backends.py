__author__ = 'elfo'
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend

class EmailBackend(SmtpEmailBackend):
    def __init__(self, **kwargs):
        super(EmailBackend, self).__init__(**kwargs)
        self.fail_silently = True