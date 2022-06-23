from email import message
from hashlib import new
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import MyUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .utlis import generate_token
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.hashers import make_password
import threading
from random import randint

def genrate_otp():
    return randint(100000,999999)


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()




class RegistrationView(View):
    def get(self, request):
        form = UserForm()
        context={'form':form}
        template_name = 'User_App/register.html'
        return render(request, template_name, context )

    def post(self, request):
        form = UserForm(request.POST)
        context = {

            'form': form,
            'has_error': False
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        password =str(request.POST.get('password'))
        confirm_password = str(request.POST.get('confirm_password'))
        if len(password) < 6:
            messages.success(request, messages.ERROR,
                                 'passwords should be atleast 8 characters long')
            context['has_error'] = True
        if password != confirm_password:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True

        try:
            if MyUser.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'User_App/register.html', context, status=400)

        
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(user.password)
            user.save()
        user = MyUser.objects.get(username=username, email=email)
        


        current_site = get_current_site(request)
        email_subject = 'Activate your Account'
        message = render_to_string('User_App/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   }
                                   )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS,
                             'account created succesfully')

        

        return redirect('login_url')   


class LoginView(View):
    def get(self, request):
        return render(request, 'User_App/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user1 = MyUser.objects.get(username=username)
            email = user1.email
        except:
            pass
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        global new
        user = authenticate(request, username=username, password=password)
        new = user
        if user1.is_verified and user is not None:
            otp = genrate_otp()
            subject = 'OTP for login to AucEasy!'
            message = f'Hi {user1},Your OTP is {otp} valid for 2 minutes!'
            email_from = settings.EMAIL_HOST_USER
            recipeint_list = [email]
            send_mail(subject,message,email_from,recipeint_list)
            response = redirect('otp_url')
            response.set_cookie('otp',otp,max_age=120)
            return response
        else:
            messages.info(request,'Please Activate Your Account First!')
            return redirect('login_url')


class OTPView(View):
    def get(self,request):
        template_name= 'User_App/otp.html'
        return render(request,template_name)
    def post(self,request):
        otp = request.POST.get('otp')
        otp1 = request.COOKIES.get('otp')
        if otp == otp1:
            login(request, new)
            return redirect('home')
        else:
            message.info(request, 'Invalid OTP!')
            return redirect('login_url')



class HomeView(View):
    def get(self, request):
        template_name = 'User_App/home.html'
        return render(request, template_name)
    




class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_verified = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('login_url')
        return render(request, 'User_App/activate_failed.html', status=401)


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login_url')


# Create your views here.
