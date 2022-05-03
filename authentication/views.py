from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

#Threading in python is used to run multiple threads (tasks, function calls) at the same time.
class EmailThread(threading.Thread):
    def __init__(self,email): #Constructor
        self.email = email
        threading.Thread.__init__(self) 
    def run(self):
        self.email.send(fail_silently=False)    

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(
            request.body
        )  # parse a valid JSON string and convert it into a Python Dictionary
        email = data["email"]
        if not validate_email(email):  # validate email
            return JsonResponse(
                {"email_error": "Email is invalid"}, status=400
            )  # return error
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "sorry email in use, please choose another one "},
                status=409,
            )
        # return true if everything is good
        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(
            request.body
        )  # parse a valid JSON string and convert it into a Python Dictionary
        username = data["username"]

        if not str(username).isalnum():  # validate username, should be alphanumeric
            return JsonResponse(
                {
                    "username_error": "username should only contain alphanumeric characters"
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "sorry username in use, choose another one "},
                status=409,
            )
        return JsonResponse(
            {"username_valid": True}
        )  # return true if everything is good


class RegistrationsView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # get user data from
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {"fieldValues": request.POST}

        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password is too short!")
                    return render(request, "authentication/register.html", context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    "user": user,
                    "domain": current_site.domain,
                    # encoded user ID
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                }

                link = reverse(
                    "activate",
                    kwargs={"uidb64": email_body["uid"],
                            "token": email_body["token"]},
                )

                email_subject = "Activate your account"

                activate_url = "http://" + current_site.domain + link

                email = EmailMessage(
                    email_subject,
                    "Hi "
                    + user.username
                    + ", Please click the link below to activate your account \n"
                    + activate_url,
                    "noreply@payment-dashboard.com",
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, "Account created successfully")
                return render(request, "authentication/register.html")

        return render(request, "authentication/register.html")
        # create a user account


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            # force text conters data to human readable format
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")

            if user.is_active:
                return redirect("login")
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully")
            return redirect("login")

        except Exception as excp:
            pass

        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, "Welcome, " + user.username
                    )
                    return redirect("expenses")
                messages.error(request, "Account is not active, please check your email")
                return render(request, "authentication/login.html")
            messages.error(request, "Invalid username-password or not actived yet!")
            return render(request, "authentication/login.html")

        messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")
    

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect("login")


class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "Please enter a valid email address")
            return render(request, 'authentication/reset-password.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():         
            email_content = {
                "user": user[0],
                "domain": current_site.domain,
                # encoded user ID
                "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
                "token": PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse(
                "set-new-password",
                kwargs={"uidb64": email_content["uid"],
                        "token": email_content["token"]},
            )

            email_subject = "Reset your password"

            reset_url = "http://" + current_site.domain + link

            email = EmailMessage(
                email_subject,
                "Hi There"
                + ", Please click the link below to reset your password \n"
                + reset_url,
                "noreply@payment-dashboard.com",
                [email],
            )
            EmailThread(email).start()
            messages.success(request, 'We sent you a reset password link')
            return render(request, 'authentication/reset-password.html', context)
        return render(request, 'authentication/reset-password.html', context)
    

class CompleteResetPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        
     
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid, Please request a new one')
                return render(request, 'authentication/reset-password.html', context)
        
        except Exception as identifier:
            pass
            
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request,'authentication/set-new-password.html',context)
        
        if len(password) <6 :
            messages.error(request, 'Password should be more than 6 characters')
            return render(request,'authentication/set-new-password.html',context)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Successfully changed your password. Please login') 
            return redirect('login')
        
        except Exception as identifier:
            messages.info(request, 'Something went wrong.') 
            return render(request,'authentication/set-new-password.html',context)    
        

    
        #return render(request,'authentication/set-new-password.html',context)    
