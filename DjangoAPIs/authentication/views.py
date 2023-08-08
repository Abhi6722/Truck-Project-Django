from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .renderers import UserRenderer
from .serializers import *
import pyotp
from .utils import Util, send_otp, EmailVerificationTokenGenerator
from .models import User, PhoneOTP
from django.utils.encoding import force_str
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import boto3
import os
import re
interval = 180


totp=pyotp.TOTP('base32secret3232',interval=interval)

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    otp = totp.now()
    
    
    email = serializer.validated_data['email']
    phone_number = serializer.validated_data['phone_number']   
    request.session['phone'] = phone_number
    
    # Send OTP via SMS
    client = boto3.client('sns', 
                          region_name='ap-south-1', 
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_SNS'), 
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_SNS'))
    
    message = f"qZense Labs \n \n Your OTP for phone number verification is {otp}"
    client.publish(PhoneNumber=phone_number, Message=message)
    serializer.save()
    user = User.objects.get(phone_number=phone_number)
    phone_otp = PhoneOTP.objects.create(
                                        phone=user,
                                        otp=otp,
                                        count=1
                                        )
    phone_otp.save()
    
    
    return Response({'message':'OTP sent to phone number'}, status=status.HTTP_201_CREATED)
    # Send Registration successful email to user's email address
    # uid = urlsafe_base64_encode(force_bytes(user.id))
    # token = PasswordResetTokenGenerator().make_token(user)
    # link = 'http://localhost:3000/activation/'+uid+'/'+token
    # body = 'Click Following Link to Activate your account: '+link
    # data = {
    #     'subject':'Registration Successful',
    #     'body':body,
    #     'to_email':user.email
    #   }
    # Util.send_email(data)
    # token = get_tokens_for_user(user)
    
    # Return success response
    # serializer.save()
    # return Response({'token':token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
  
class VerifyOTPView(APIView):
    # permission_classes = (AllowAny,)
    
    def post(self, request):
        phone = request.session.get('phone')
        otp = request.data.get('otp')
        if otp:
            try:
                phone_obj = PhoneOTP.objects.get(phone=phone)
                if totp.verify(otp): # phone_obj.otp == otp:
                    # Verify the OTP
                    phone_obj.validated = True
                    phone_obj.save()
                    # Mark phone number as verified in User model
                    user = User.objects.get(phone_number=phone)
                    user.phone_verified = True
                    user.save()
                    # Clear phone number from session data
                    del request.session['phone']
                    
                    uid = urlsafe_base64_encode(force_bytes(user.id))
                    token = EmailVerificationTokenGenerator().make_token(user)
                    link = 'http://127.0.0.1:8000/api/user/verify-email/'+uid + '/'+ token
                    body = 'Click Following Link to Activate your account: '+link
                    data = {
                        'subject':'Registration Successful',
                        'body':body,
                        'to_email':user.email
                      }
                    Util.send_email(data)
                    token = get_tokens_for_user(user)
                    
                    return Response({'message': 'Phone Number verified successfully'}, status = status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Invalid OTP'}, status = status.HTTP_403_FORBIDDEN)
            except PhoneOTP.DoesNotExist:
                return Response({'error': 'Invalid phone number'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'error': 'OTP is required'}, status = status.HTTP_400_BAD_REQUEST)
          
class ResendEmailView(APIView):
  def post(self, request):
    email_address = request.data.get('email')
    # print(email_address, len(email_address))
    if not len(email_address):
      return Response({'message': 'Please enter your email address'}, status = status.HTTP_400_BAD_REQUEST)
    
    if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email_address):
      return Response({'message': 'Email address in wrong format'}, status = status.HTTP_400_BAD_REQUEST)
    
    try:
      user = User.objects.get(email=email_address)
      if user.email_verified:
        return Response({'message':'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = EmailVerificationTokenGenerator().make_token(user)
      link = 'http://localhost:3000/api/user/verify-email/'+uid + '/'+ token
      body = 'Click Following Link to Activate your account: '+link
      data = {
          'subject':'Email verification',
          'body':body,
          'to_email':user.email
        }
      Util.send_email(data)
      return Response({'message': 'Email sent successfully'}, status = status.HTTP_202_ACCEPTED)
    except User.DoesNotExist:
      return Response({'message':'Email address not registered'}, status=status.HTTP_404_NOT_FOUND)
    
class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        uidb64 =  kwargs.get('uid')
        token =  kwargs.get('token')
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=uid)
        except User.DoesNotExist:
          return Response({'error': "User Doesn't exist"}, status = status.HTTP_404_NOT_FOUND)
        
        if EmailVerificationTokenGenerator().check_token(user, token):
          user.email_verified = True # Set the email_verified field to True
          user.save() # Save the updated user object to the database
          return redirect('http://3.111.145.93/login.html')
          # return Response({'success': 'Email verified successfully'}, status = status.HTTP_200_OK)
        
        else:
          return Response({'message': 'Invalid Token'}, status = status.HTTP_400_BAD_REQUEST)
        
          
class PhoneValidationView(APIView): 
  def post(self, request):
    phone = request.data.get('phone')
    if len(phone) > 15:
      return Response({'message':'Invalid phone number'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
      user = User.objects.get(phone_number = phone)
      return_type = send_otp(phone)
      if return_type:
        request.session['phone'] = phone
        return HttpResponse("OTP sent successfully")
      else:
        return HttpResponseForbidden("Maximum OTP limit reached")
        
    except User.DoesNotExist:
      # return status = 404 not found
      return HttpResponseNotFound('Phone number is not registered')
    

class ResendOTPView(APIView):
  def get(self, request):
    phone_number = request.session['phone']
    # print(phone_number)
    try:
      user = User.objects.filter(phone_number=phone_number).first()
      if user and send_otp(phone_number):
          return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)
      else:
        return Response({'message': 'Maximum OTP limit reached, Please contact support'}, status=status.HTTP_429_TOO_MANY_REQUESTS) 
    except User.DoesNotExist:
      return Response({'message': 'Phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)
           

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    # print(user.first_name)
    if user is not None and user.phone_verified and user.email_verified: # and user is active
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    elif user is None:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_401_UNAUTHORIZED)
    elif not user.phone_verified:
      return Response({'message':'Phone number not verified'}, status = status.HTTP_403_FORBIDDEN)
    else:
      return Response({'message':'email address not verified'}, status = status.HTTP_403_FORBIDDEN)
    
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
  
  
class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    # serializer = SendPasswordResetEmailSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)   
    # return Response({'msg':'Password Reset link sent. Please check your Email'}, status=status.HTTP_200_OK)
    """
    Send password reset email to the user
    """
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        link = 'http://localhost:3000/api/user/reset-password-verification/'+uid+'/'+token
        body = 'Click Following Link to Reset Your Password '+link
        data = {
          'subject':'Reset Your Password',
          'body':body,
          'to_email':user.email
        }
        Util.send_email(data)
        request.session['uid'] = uid
        request.session['token'] = token
        return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'User with this email not found'}, status=status.HTTP_400_BAD_REQUEST)
  
class PasswordResetVerifyAPIView(APIView):
    def get(self, request, uid, token):
        if not uid or not token:
            return Response({'detail': 'Password reset link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_bytes(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Password reset link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'detail': 'Password reset link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # Password reset link is valid
        return redirect('https://www.youtube.com/')
 
class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    uid = request.session.get('uid')
    token = request.session.get('token')
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    del request.session['uid']
    del request.session['token']
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)       
  
# class UserPasswordResetView(APIView):
# renderer_classes = [UserRenderer]
# def post(self, request, uid, token, format=None):
#   serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#   serializer.is_valid(raise_exception=True)
#   return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)