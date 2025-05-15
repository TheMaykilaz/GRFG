from django.shortcuts import render

main_menu = [
    {'name': 'Головна', 'url_name': 'home'},
    {'name': 'Дізнатися', 'url_name': 'explore'},
    {'name': 'Про нас', 'url_name': 'about'},
    {'name': 'Реєстрація', 'url_name': 'account:registration'},
    {'name': 'Вхід', 'url_name': 'account:login'},
    {'name': 'Налаштування', 'url_name': 'account:settings'},
]

explore_menu = [
    {'name': 'Форум', 'url_name': 'forum'},
    {'name': 'Статті', 'url_name': 'articles'},
    {'name': 'БрейкінгНьюс', 'url_name': 'news'},
]