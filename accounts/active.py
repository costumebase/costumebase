from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.views.decorators.http import require_http_methods
from .tokens import account_activation_token, cutomer_account_token
from django.utils.http import urlsafe_base64_decode

from .models import User, Vendor, Buyer


@require_http_methods(["GET"])
def activate(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # now we're activating the user
     # and we're changing the boolean field so that the token link becomes invalid
        user.save()
        # bar = Vendor.objects.get(pk=pk)
        # bar.email_confirmed = True
        # bar.save()
        login(request, user)  # log the user in
        messages.add_message(request, messages.INFO, 'Hi {0} please login to your account.'.format(request.user.first_name))
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('register:vendor_login')


@require_http_methods(["GET"])
def activate_customer(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and cutomer_account_token.check_token(user, token):
        user.is_active = True  # now we're activating the user
     # and we're changing the boolean field so that the token link becomes invalid
        user.save()
        # bar = Vendor.objects.get(pk=pk)
        # bar.email_confirmed = True
        # bar.save()
        login(request, user)  # log the user in
        messages.add_message(request, messages.INFO, 'Hi {0} please login to your account.'.format(request.user.buyer.your_name))
    else:
        messages.add_message(request, messages.WARNING, 'Account activation link is invalid.')

    return redirect('register:customer_login')