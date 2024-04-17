import hashlib
from random import sample
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser as User

def hash_otp(user: User) -> str:
    type(user) == User, f'OTP must be string and user must be an instance of {User}'
    otp_string = user.username + user.email
    return hashlib.sha256(bytes(otp_string, encoding='utf-8')).hexdigest()

# generate and cache OTP
def generate_otp(user: User) -> str:
    assert type(user) == User, f'user must be an instance of {User}'
    otp = ''.join(str(i) for i in sample(range(0, 10), 6))
    otp_hash = hash_otp(otp, user)

    if cache.has_key(otp_hash):
        cached_otp = cache.get(otp_hash)
        print('cached_otp')
        return cached_otp
    else:
        cached_otp = cache.add(otp_hash, otp)
        print('new-otp')
        return otp

# custom function for sending any email
def send_mail(mail_func: callable, *args) -> Response:
    assert callable(mail_func), f'{mail_func} must be a function'
    
    try:
        mail_func(*args)
        return Response({
            'response': 'email sent'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({
            'response': 'an error occured'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)