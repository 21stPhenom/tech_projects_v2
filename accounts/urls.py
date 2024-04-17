from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.accounts_list, name='accounts-list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('<str:username>/', views.account_detail, name='account-detail'),
    path('<str:username>/delete/', views.delete_account, name='delete-account'),
]