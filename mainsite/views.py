from django.shortcuts import render
from blacklist.menu_data import main_menu


def home(request):
    context = {
        'title': 'home',
        'main_menu': main_menu, 
        'home_menu': [item for item in main_menu if item['name'] in ['Головна', 'Дізнатися', 'Про нас']]
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {'menu': main_menu,
                                          'title': 'about'})



