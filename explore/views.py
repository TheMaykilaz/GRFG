from django.http import HttpResponse
from django.shortcuts import render
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
    }
    return render(request, 'explore.html', context)



class CryptoTokenListAPI(APIView):
    def get(self, request):
        get_top_cryptos()
        tokens = CryptoToken.objects.all().values(
            'name', 'symbol', 'price', 'percent_1h',
            'percent_24h', 'percent_7d', 'market_cap', 'volume_24h'
        )
        return Response(list(tokens))


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

    # Перевірка на наявність статті за ID
    article = next((article for article in articles if article['id_a'] == article_id), None)

    if article:
        paragraph = text_in_article(article)
    else:
        return HttpResponseNotFound("Статтю не знайдено")

    context = {
        'menu': explore_menu,
        'article': article,
        'paragraph': paragraph,
    }
    return render(request, 'articles_page.html', context)



@login_required
def forum(request):
    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent = None
            if parent_id:
                parent = get_object_or_404(ForumComment, id=parent_id)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.parent = parent
            comment.save()
            return redirect('explore:forum')
    else:
        form = ForumCommentForm()

    comments = ForumComment.objects.filter(parent__isnull=True).order_by('-created_at').prefetch_related('replies')
    context = {
        'menu': explore_menu,
        'title': 'Forum',
        'comments': comments,
        'form': form,
    }
    return render(request, 'forum.html', context)



@login_required
def vote_comment(request, comment_id, vote_type):
    comment = get_object_or_404(ForumComment, id=comment_id)
    user = request.user

    if vote_type == 'up':
        if user in comment.downvotes.all():
            comment.downvotes.remove(user)
        if user in comment.upvotes.all():
            comment.upvotes.remove(user)
        else:
            comment.upvotes.add(user)

    elif vote_type == 'down':
        if user in comment.upvotes.all():
            comment.upvotes.remove(user)
        if user in comment.downvotes.all():
            comment.downvotes.remove(user)
        else:
            comment.downvotes.add(user)

    return JsonResponse({'score': comment.score()})


def index(request):
    return render(request, 'explore/index.html')