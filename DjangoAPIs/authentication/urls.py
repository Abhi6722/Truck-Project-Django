from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/<uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend_email/', ResendEmailView.as_view(), name = 'resend_email_verification'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verifyOTP'),
    path('resend_otp/', ResendOTPView.as_view(), name='resendOTP'),
    path('phone_validation/', PhoneValidationView.as_view(), name='phone_verification'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset-password'),
    path('reset-password-verification/<uid>/<token>/', PasswordResetVerifyAPIView.as_view(), name='reset-password-link'),
    # path('reset-password/', UserPasswordResetView.as_view(), name='reset-password'),
]