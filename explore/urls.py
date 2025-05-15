from django.urls import path
from . import views
from django.urls import path
from explore.views import CryptoTokenListAPI
from explore.views import *
from .views import IndexDataAPI

app_name = 'explore'

urlpatterns = [
    path('', views.explore, name='explore'),
    path('forum/', views.forum, name='forum'),
    path('articles/', views.articles, name='articles'),
    path('news/', views.news, name='news'),
    path('api/cryptos/', CryptoTokenListAPI.as_view(), name='crypto-list-api'),
    path('articles/<int:article_id>/', views.articles_page, name='articles-page'),
    path('api/index-data/', IndexDataAPI.as_view(), name='get_index_data_api'),




]
