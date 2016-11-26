from django.conf.urls import url, include
from django.contrib import admin
from apps.client import views

urlpatterns = [
    url('api/connect/', views.ConnectView.as_view(), name='login'),
    url('api/verify/', views.VerifyView.as_view(), name='verify'),
    url('accounts/profile/', views.AccountProfile.as_view(), name='account_profile'),
    url('register/', views.RegistrationView.as_view(), name='register'),
    url('users/', views.UserView.as_view(), name='user'),
    url(r'^$', views.RegistrationView.as_view(), name='user'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
]

