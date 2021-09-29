from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.vendor.email_confirmed)
        )

class CustomerAccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.buyer.email_confirmed)
        )


class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.vendor.reset_password)
        )


account_activation_token = AccountActivationTokenGenerator()
cutomer_account_token = CustomerAccountActivationTokenGenerator()
password_reset_token = PasswordResetToken()