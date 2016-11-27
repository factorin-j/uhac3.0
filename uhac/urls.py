from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url('api/connect/', views.ConnectView.as_view(), name='api.login'),
    url('api/verify/', views.VerifyView.as_view(), name='api.verify'),
    url('records/create/', views.CriminalRecordCreateView.as_view(), name='records.create'),
    url('records/', views.CriminalRecordView.as_view(), name='records.list'),
    url('register/', views.RegistrationView.as_view(), name='register'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
]

