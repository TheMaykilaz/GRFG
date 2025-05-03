from django.shortcuts import render
from blacklist.menu_data import main_menu


def home(request):

    return render(request, 'home.html', {'menu': main_menu,
                                         'title': 'home'})

def about(request):
    return render(request, 'about.html', {'menu': main_menu,
                                          'title': 'about'})

