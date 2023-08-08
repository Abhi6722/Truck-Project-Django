from django.core.mail import EmailMessage
from .models import User, PhoneOTP
import os
import boto3
import pyotp
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.is_active) + str(user.pk) + str(timestamp)
        )


# email_verification_token = EmailVerificationTokenGenerator()

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']],
    )
    email.send()



def generate_otp():
  totp=pyotp.TOTP('base32secret3232',interval=180)
  otp = totp.now()
  return otp

def send_otp(phone_number):
    user = User.objects.get(phone_number=phone_number)
    # if user:
    try:
        phone_otp = PhoneOTP.objects.get(phone=user)
        if phone_otp.count > 10:
            return False #"Maximum OTP attempts reached")
        else:
            phone_otp.otp = generate_otp()
            phone_otp.count += 1
    except PhoneOTP.DoesNotExist:
        phone_otp = PhoneOTP.objects.create(phone=user, otp=generate_otp(), count=1)
    phone_otp.save()
    client = boto3.client('sns', 
                      region_name='ap-south-1', 
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_SNS'), 
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_SNS'))
    message = f"qZense Labs \n \n Your OTP for phone number verification is {phone_otp.otp}"
    client.publish(PhoneNumber=phone_number, Message=message)
    return True
    # else:
    #     return False