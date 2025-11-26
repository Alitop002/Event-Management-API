from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status as st
import re

def send_code_to_email(email, code):
    text = f"""
        Hello!

        You requested a verification code for your TwitterAPI account.

        Your verification code is: {code}

        Enter this code in the app to verify your email address.

        If you didn't request this code, you can ignore this email.

        Best regards,
        TwitterAPI Team
        """
    send_mail(
        subject="Your Verificated Code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )

class CustmResponse:
    @staticmethod
    def success(message, status=False, data=None):
        data = {
            "status":status,
            "message":message,
            "data": data
        }
        return Response(
            data=data,
            status=st.HTTP_200_OK
        )
    
    @staticmethod
    def error(message, status=False, data=None):
        data = {
            "status":status,
            "message":message,
            "data": data
        }
        return Response(
            data=data,
            status=st.HTTP_400_BAD_REQUEST
        )
    
    