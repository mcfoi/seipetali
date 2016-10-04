import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator


__all__ = ('TokenGenerator', 'token_generator')


## A simple token generator.
#
#  The "PasswordResetTokenGenerator" in Django is great, but it needs
#  a couple of methods to be overridden to make it a little easier to
#  use.
#
class TokenGenerator(PasswordResetTokenGenerator):

    def _num_days(self, dt):
        return (dt - datetime.datetime(2001,1,1)).seconds

    def _today(self):
        return datetime.datetime.now()


# Declare a global token generator.
token_generator = TokenGenerator()
