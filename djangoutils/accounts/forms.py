from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from djangoutils.uniform import make_helper, UniFormMedia


class AuthenticationForm(DjangoAuthenticationForm, UniFormMedia):

    @property
    def helper(self):
        return make_helper(self, (('login', 'Login'),), (('cancel', 'Cancel'),))
