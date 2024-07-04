from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.emails import otp_mail
from accounts.models import CustomUser as User
from accounts.permissions import IsOwner
from accounts.serializers import CustomUserSerializer as UserSerializer
from accounts.utils import generate_otp, hash_otp, send_mail

class Accounts(APIView):
    model = User
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = self.model.objects.all()
        queryset = self.serializer_class(queryset, many=True)
        
        return Response(queryset, status=status.HTTP_200_OK)

class AccountDetail(APIView):
    model = User
    serializer_class = UserSerializer
    
    def get(self, request, username, *args, **kawrgs):
        user = get_object_or_404(User, username=username)
        user = self.serializer_class(user)
        return Response(user.data, status=status.HTTP_200_OK)

class Register(APIView):
    model = User
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        user = self.serializer_class(data=request.data)
        
        if user.is_valid():
            user.save()
            token = Token.objects.get_or_create(user=user.data['id'])
            
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    model = User
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        password = request.data['password']
        username = request.data.get('username', None)
        email = request.data.get('email', None)

        if email == None and username != None:
            user = authenticate(request, username=username, password=password)
        elif username == None and email != None:
            user = authenticate(request, email=email, password=password)
        else:
            return Response({
                'error': 'either email or username must be provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user is not None:
            token = Token.objects.get(user=user).key
            return Response({
                'token': token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'invalid credentials provided'
            }, status=status.HTTP_400_BAD_REQUEST)

class ForgotPassword(APIView):
    def get(self, request, *args, **kwargs):
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        otp = generate_otp(user)
        
        return send_mail(otp_mail, email, otp)
    
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        otp = request.data['otp']
        
        otp_hash = hash_otp(user, otp)
        if cache.has_key(otp_hash) and cache.get(otp_hash) == otp:
            return Response({
                'response': otp_hash
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
            
class ResetPassword(APIView):
    def post(self, request, *args, **kwargs):
        otp_hash = request.data['otp_hash']            
        email = request.data['email']
        new_password = request.data['password']
        user = get_object_or_404(User, email=email)
        
        if cache.has_key(otp_hash):
            user.password = make_password(new_password)
            user.save()
            cache.delete(otp_hash)
            
            return Response({
                'response': 'password updated'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'invalid OTP hash'
            }, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        otp = generate_otp(user)
        return send_mail(otp_mail, user.email, otp)
    
    def delete(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        otp = request.data['otp']
        otp_hash = hash_otp(user, otp)
        
        if cache.has_key(otp_hash) and cache.get(otp_hash) == otp:
            user.delete()
            cache.delete(otp_hash)
            
            return Response({
                'response': 'account deleted'    
            },status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'error': 'invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)

accounts_list = Accounts.as_view()
account_detail = AccountDetail.as_view()
register = Register.as_view()
login = Login.as_view()
forgot_password = ForgotPassword.as_view()
reset_password = ResetPassword.as_view()
delete_account = DeleteAccount.as_view()