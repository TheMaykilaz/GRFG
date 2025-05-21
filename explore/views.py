from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CryptoToken
from explore.models import CryptoToken
from blacklist.menu_data import explore_menu
from blacklist.parser_bitcoin import *
from blacklist.explore_page import *
from blacklist.article_news import *
from blacklist.yahoo_indexis import *
from django.http import JsonResponse
from .forms import ForumCommentForm
from .models import ForumComment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from explore.models import CryptoToken
from rest_framework.serializers import ModelSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CryptoToken
from .serializers import CryptoTokenSerializer
from .filters import CryptoTokenFilter
from .models import ForumTopic
from .forms import ForumTopicForm
from django.views.generic import DetailView
from django.http import HttpResponseNotFound

def explore(request):
    dominance_data = get_cryptocurrency_dominance()
    total_cap = get_total_dominance()
    fg = get_fear_and_greed()

    context = {
        'title': 'Explore',
        'menu': explore_menu,
        'alldom': dominance_data.to_html(index=False, classes="dom-table"),
        'total_cap': total_cap,
        'fg': fg,
        'crypto_detail_url': reverse('explore:crypto-detail', kwargs={'symbol': 'REPLACE'}).replace('REPLACE', ''),
    }
    return render(request, 'explore.html', context)



class CryptoTokenSerializer(ModelSerializer):
    class Meta:
        model = CryptoToken
        fields = ['name', 'symbol', 'price', 'percent_1h', 'percent_24h', 'percent_7d', 'market_cap', 'volume_24h']

class CryptoTokenListAPI(generics.ListAPIView):
    queryset = CryptoToken.objects.all().order_by('-market_cap')
    serializer_class = CryptoTokenSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CryptoTokenFilter
    search_fields = ['name', 'symbol']
    ordering_fields = ['price', 'market_cap', 'percent_1h', 'percent_24h', 'percent_7d', 'volume_24h', 'sparkline_7d']


def news(request):
    return render(request, 'news.html', {'menu': explore_menu,

                                         'title': 'news'}  )
def articles(request):
    articles = list_of_articles()

    context = {
        'menu': explore_menu,
        'articles': articles,
    }

    return render(request, 'articles.html', context )

def articles_page(request, article_id):
    articles = list_of_articles()
    article = next((article for article in articles if article['id_a'] == article_id), None)

    if article:
        article_content = text_in_article(article)
        paragraph = article_content['text']
        author = article_content['author']
    else:
        return HttpResponseNotFound("Статтю не знайдено")

    context = {
        'menu': explore_menu,
        'article': article,
        'paragraph': paragraph,
        'author': author,
    }
    return render(request, 'articles_page.html', context)

class CryptoDetailView(DetailView):
    template_name = 'explore/crypto_detail.html'  # Correct path to template
    context_object_name = 'crypto'
    
    def get_object(self):
        symbol = self.kwargs.get('symbol').upper()
        return get_object_or_404(CryptoToken, symbol=symbol)

# @login_required
# def forum(request):
#     if request.method == 'POST':
#         form = ForumCommentForm(request.POST)
#         if form.is_valid():
#             parent_id = request.POST.get('parent_id')
#             parent = None
#             if parent_id:
#                 parent = get_object_or_404(ForumComment, id=parent_id)

#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.parent = parent
#             comment.save()
#             return redirect('explore:forum')
#     else:
#         form = ForumCommentForm()

#     comments = ForumComment.objects.filter(parent__isnull=True).order_by('-created_at').prefetch_related('replies')
#     context = {
#         'menu': explore_menu,
#         'title': 'Forum',
#         'comments': comments,
#         'form': form,
#     }
#     return render(request, 'forum.html', context)




def forum_topic_list(request):
    topics = ForumTopic.objects.order_by('-created_at')
    return render(request, 'forum/topic_list.html', {'topics': topics})

def forum_topic_detail(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    comments = topic.forumcomment_set.order_by('created_at')  
    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'comments': comments
    })

@login_required
def add_comment(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            ForumComment.objects.create(topic=topic, user=request.user, content=content)
    return redirect('explore:forum-topic-detail', pk=pk)

def vote_comment(request, comment_id):
    comment = get_object_or_404(ForumComment, id=comment_id)
    vote_type = request.POST.get('vote_type')  # 'upvote' або 'downvote'
    
    if vote_type not in ['upvote', 'downvote']:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)

    is_upvote = True if vote_type == 'upvote' else False

    vote, created = ForumCommentVote.objects.get_or_create(
        user=request.user,
        comment=comment,
        defaults={'is_upvote': is_upvote}  # ⬅️ обов'язково додаємо
    )

    if not created:
        if vote.is_upvote == is_upvote:
            # повторне голосування → прибираємо голос
            vote.delete()
        else:
            # змінюємо голос
            vote.is_upvote = is_upvote
            vote.save()

    return redirect('explore:forum-topic-detail', pk=comment.topic.pk)

@login_required
def create_forum_topic(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('explore:forum-topic-list')
    else:
        form = ForumTopicForm()
    return render(request, 'forum/create_topic.html', {'form': form})

#
@login_required
def vote_comment_js(request, comment_id, vote_type):
    comment = get_object_or_404(ForumComment, pk=comment_id)
    is_upvote = vote_type == 'up'

    vote, created = ForumCommentVote.objects.get_or_create(user=request.user, comment=comment)
    if not created and vote.is_upvote == is_upvote:
        vote.delete()
        comment.vote_count += -1 if is_upvote else 1
    else:
        vote.is_upvote = is_upvote
        vote.save()
        comment.vote_count += 1 if is_upvote else -1
    comment.save()
    return JsonResponse({'score': comment.vote_count})