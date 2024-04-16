from django.core.mail import EmailMessage
from django.conf import settings

def otp_mail(address: str, otp: str):
    otp_mail = EmailMessage(
        'OTP from Tech Projects',
        f'Here is your One Time Password: {otp}. This OTP is valid for 15 minutes only.',
        settings.DEFAULT_FROM_EMAIL,
        [address]
    )
    return otp_mail.send()