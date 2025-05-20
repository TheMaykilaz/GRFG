from django.urls import path
from . import views
from django.urls import path
from explore.views import CryptoTokenListAPI
from explore.views import *
from .views import IndexDataAPI
from .models import *

app_name = 'explore'

urlpatterns = [
    path('', views.explore, name='explore'),
    path('forum/', views.forum_topic_list, name='forum'),
    path('articles/', views.articles, name='articles'),
    path('news/', views.news, name='news'),
    path('api/cryptos/', CryptoTokenListAPI.as_view(), name='crypto-list-api'),
    path('articles/<int:article_id>/', views.articles_page, name='articles-page'),
    path('api/index-data/', IndexDataAPI.as_view(), name='get_index_data_api'),
    path('forum/<int:pk>/', views.forum_topic_detail, name='forum-topic-detail'),
    path('forum/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/vote/', views.vote_comment, name='vote-comment'),
    path('forum/topics/', views.forum_topic_list, name='forum-topic-list'),
    path('forum/new/', views.create_forum_topic, name='create-forum-topic'),
    path('forum/<int:pk>/', views.forum_topic_detail, name='forum-topic-detail'),
    path('crypto/<str:symbol>/', views.CryptoDetailView.as_view(), name='crypto-detail'),
    
    #path("forum/vote/<int:comment_id>/<str:vote_type>/", views.vote_comment, name="vote_comment"),
#
    path("forum/vote/<int:comment_id>/<str:vote_type>/", views.vote_comment_js, name="vote_comment"),



]
