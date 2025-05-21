from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_view, name='logout'),
]