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



def forum(request):
    comments = ForumComment.objects.order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ForumCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                form = ForumCommentForm()  # очистити форму після відправки
        else:
            form = None  # неавторизований користувач
    else:
        form = ForumCommentForm() if request.user.is_authenticated else None

    context = {
        'title': 'Форум',
        'menu': explore_menu,
        'form': form,
        'comments': comments,
    }
    return render(request, 'forum.html', context)

def index(request):
    return render(request, 'explore/index.html')
