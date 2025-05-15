from django.shortcuts import render

main_menu = [
    {'name': 'Головна', 'url_name': 'mainsite:home'},
    {'name': 'Дізнатися', 'url_name': 'explore:explore'},
    {'name': 'Про нас', 'url_name': 'mainsite:about'},
    {'name': 'Реєстрація', 'url_name': 'account:registration'},
    {'name': 'Вхід', 'url_name': 'account:login'},
    {'name': 'Налаштування', 'url_name': 'account:settings'},
]


explore_menu = [
    {'name': 'Форум', 'url_name': 'explore:forum'},
    {'name': 'Статті', 'url_name': 'explore:articles'},
    {'name': 'БрейкінгНьюс', 'url_name': 'explore:news'},
]