from django.urls import path
from . import views
from django.urls import path, include  # Додай include

app_name = 'mainsite'

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка
    path('about/', views.about, name='about'),
    path('explore/', include('explore.urls')),
    path('account/', include('account.urls')),


]
