from django.conf import settings
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PID(PasswordResetTokenGenerator):
    def _make_hash_value(self, product):
        return (six.text_type(product.id) + six.text_type(product.pubdate))
    def _make_token_with_timestamp(self, product, timestamp):
        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(product),
        ).hexdigest()[::2]
        return "%s-%s" % (product.id, hash)

pid = PID()
