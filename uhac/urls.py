from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url('api/connect/', views.ConnectView.as_view(), name='api.login'),
    url('api/verify/', views.VerifyView.as_view(), name='api.verify'),
    url('accounts/profile/', views.AccountsProfileView.as_view(), name='account_profile'),
    url('register/', views.RegistrationView.as_view(), name='register'),
    url(r'^$', views.RootView.as_view(), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
]

