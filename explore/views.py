from django.shortcuts import render
from whitelist.menu_data import explore_menu
from whitelist.parser_bitcoin import *
from whitelist.explore_page import *


alldom = get_cryptocurrency_dominance()
total_cap = get_total_dominance()
fg = get_fear_and_greed()
datacrypto = get_top_cryptos()


def explore(request):
    dominance_html = alldom.to_html(classes="table table-striped", index=False, border=0)
    crypto_html = datacrypto.to_html(classes="table table-striped", index=False, border=0)
    return render(request, 'explore.html',
                  {'menu': explore_menu,
                            'title': 'explore', 'alldom': dominance_html, 'total_cap': total_cap, 'fg': fg, 'datacrypto': crypto_html} )

def news(request):
    return render(request, 'news.html', {'menu': explore_menu,

                                         'title': 'news'}  )
def articles(request):
    return render(request, 'articles.html', {'menu': explore_menu,
                                             'title': 'articles'

                                             } )
def forum(request):
    return render(request, 'forum.html', {'menu': explore_menu,
                                          'title': 'forum'} )

