from .views import RegistrationsView, UsernameValidationView, LoginView,LogoutView, EmailValidationView, VerificationView,ResetPasswordView,CompleteResetPassword
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationsView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate-email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('set-new-password/<uidb64>/<token>', CompleteResetPassword.as_view(), name='set-new-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
]
