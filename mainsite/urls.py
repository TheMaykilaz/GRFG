from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Головна сторінка
    path('about/', views.about, name='about'),  # Сторінка Про нас

]
