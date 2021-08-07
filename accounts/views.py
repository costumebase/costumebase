from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect


from django.views.generic import TemplateView, CreateView
from .models import User, Buyer, Vendor, UserOTP

from .forms import CustomerSignUpForm, VendorSignUpForm, CodeForm

import random

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.views.decorators.http import require_http_methods

from .tokens import account_activation_token, cutomer_account_token
# from project.decorators import check_recaptcha

from costumebase.settings import SENDGRID_API_KEY

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import User, Code
from django.contrib.auth.forms import AuthenticationForm

from costumebase import settings

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from .utlis import send_sms

# send_mail('Subject testing testing', 'Here is the message.', 'rafik5565@gmail.com', ['alenrafi1511@gmail.com'], fail_silently=False)
# @check_recaptcha




def auth_view(request):
    form = AuthenticationForm
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('register:verify')
        # else:
        #     messages.error(request,'Please check your email to active account.')
        elif user and user.is_active:
            request.session['pk'] = user.pk
            return redirect('register:verify')
        else:
            messages.error(request,'You have entered an invalid username or password.')
            return redirect('register:vendor_login')
    return render(request, 'auth.html', {'form': form})


def sms_verify(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.email}: {user.code}"
        if not request.POST:
            print(code_user)
            send_sms(code_user, user.phone)

        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('dashboard:index')
            else:
                messages.error(request,'Wrong Code')
                return redirect('register:vendor_login')
    return render(request, 'verify.html', {'form': form})



         



class Vendor_Registration_Index(TemplateView):
    template_name = 'vendor/index.html'


@require_http_methods(["GET", "POST"])
def vendor_register(request):
    """Register new users and send verification mails to their email addresses."""
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid(): # checking the form and RECAPTCHA with decorator
            email = request.POST.get('email')
            # site = get_current_site(request) # for the domain
            site = get_current_site(request) # for the domain
            user = form.save() # add all information from the form in the User model
            user.is_active = False  # user is only active after confirming the email!
            user.save() # save the User model
            
            # subject = 'Activate Your Metro shop Account'

            message = render_to_string('registration/activate_account_mail.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })  # filling the  activation mail template w/ all the variables 

            # message = render_to_string('registration/activate_account_mail.html', {
            #     'user': user,
            #     'domain': '127.0.0.1:8000',
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })


            # This part can be found in the SendGrid setup guide as well
            message = Mail(
                from_email='rafik5565@gmail.com',
                to_emails=email,
                subject='Activate account for domain.com',
                html_content=message)

            # user.email_user(subject, message)
            # return render(request, 'registration/home2.html', {'subject': message})
            
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY) # config file where I keep my keys
                response = sg.send(message)  # .status_code, .body, .headers
                messages.add_message(request, messages.SUCCESS, 'A verification email has been sent.')
                messages.add_message(request, messages.WARNING, 'Please also check your SPAM inbox!')

            except Exception as e:
                print(e)  # e.message
                messages.add_message(request, messages.WARNING, str(e))
        else:
            return render(request, 'registration/signup.html', {'form': form})

    return render(request, 'registration/signup.html', {'form': VendorSignUpForm()})


@require_http_methods(["GET", "POST"])
def customer_register(request):
    """Register new users and send verification mails to their email addresses."""
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid(): # checking the form and RECAPTCHA with decorator
            email = request.POST.get('email')
            # site = get_current_site(request) # for the domain
            site = get_current_site(request) # for the domain
            user = form.save() # add all information from the form in the User model
            user.is_active = False  # user is only active after confirming the email!
            user.save() # save the User model
            
            # subject = 'Activate Your Metro shop Account'

            message = render_to_string('registration/activate_customer_account_mail.html', {
                'user': user,
                'protocol': 'http',
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': cutomer_account_token.make_token(user),
            })  # filling the  activation mail template w/ all the variables 

            # message = render_to_string('registration/activate_account_mail.html', {
            #     'user': user,
            #     'domain': '127.0.0.1:8000',
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })


            # This part can be found in the SendGrid setup guide as well
            message = Mail(
                from_email='rafik5565@gmail.com',
                to_emails=email,
                subject='Activate account for domain.com',
                html_content=message)

            # user.email_user(subject, message)
            # return render(request, 'registration/home2.html', {'subject': message})
            
            try:
                sg = SendGridAPIClient(SENDGRID_API_KEY) # config file where I keep my keys
                response = sg.send(message)  # .status_code, .body, .headers
                messages.add_message(request, messages.SUCCESS, 'A verification email has been sent.')
                messages.add_message(request, messages.WARNING, 'Please also check your SPAM inbox!')

            except Exception as e:
                print(e)  # e.message
                messages.add_message(request, messages.WARNING, str(e))
        else:
            return render(request, 'registration/customer_signup.html', {'form': form})

    return render(request, 'registration/customer_signup.html', {'form': CustomerSignUpForm()})



def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')






































def signugggp(request):
    if request.method == 'POST':
        form = VendorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = '127.0.0.1:8000'
            subject = 'Activate Your Metro shop Account'
            message = render_to_string('metroshop/account_activation_email.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })


            user.email_user(subject, message)
            return render(request, 'metroshop/home2.html', {'subject': message})
    else:
        form = SignUpForm()
    return render(request, 'metroshop/signup.html', {'form': form})


class Acc(TemplateView):

    template_name = 'registration/index.html'




class VendorSignUpView(CreateView):
    model = Vendor
    form_class = VendorSignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')








# def signup(request):
#     if request.method == 'POST':
#         get_otp = request.POST.get('otp')
#         print(get_otp)

#         if get_otp:
#             get_user = request.POST.get('user')
#             user = User.objects.get(email=get_user)
#             if int(get_otp) == UserOTP.objects.filter(user = user).last().otp:
#                 user.is_active = True
#                 user.save()
#                 messages.success(request, f'Account is Created For {user.email}')
#                 return redirect('login')
#             else:
#                 messages.warning(request, f'You Entered a Wrong OTP')
#                 return render(request, 'registration/signup.html', {'otp': True, 'user': user})

#         form = VendorSignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             user = User.objects.get(email=email)
#             print(user)
#             user.email = email
#             user.is_active = False
#             user.save()
#             usr_otp = random.randint(100000, 999999)
#             UserOTP.objects.create(user=user, otp = usr_otp)
#             mess = f"Hello {user.email},\nYour OTP is {usr_otp}\nThanks!"

#             send_mail( 'Welcome to Costume Base - Verify Your Email', 
#             mess , settings.DEFAULT_FROM_EMAIL, [user.email], 
#             fail_silently = False)

#             return render(request, 'registration/signup.html', {'otp': True, user: user})  
#     else:
#         form = VendorSignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})  


    
