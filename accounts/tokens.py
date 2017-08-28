from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Ensure results are consistent across DB backends
        login_timestamp = ''
        return (
            six.text_type(user.pk) + user.password + six.text_type(login_timestamp) + six.text_type(timestamp)
        )

account_activation_token = AccountActivationTokenGenerator()
