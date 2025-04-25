from django.urls import path
from . import views

urlpatterns = [
    path('', views.explore, name='explore'),
    path('forum/', views.forum, name='forum'),
    path('articles/', views.articles, name='articles'),
    path('news/', views.news, name='news'),

]
