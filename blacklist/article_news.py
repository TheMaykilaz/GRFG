import requests
from bs4 import BeautifulSoup
import re
import random

def list_of_articles():
    url = "https://incrypted.com/ua/novyny/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    articles = []

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title_blocks = soup.find_all('div', class_='incr_loop-title hide-mobile-only-flex')

        for idx, block in enumerate(title_blocks, start=1):
            a_tag = block.find('a')
            if a_tag:
                article_url = a_tag['href'].strip()
                article_title = a_tag.text.strip()

                # Пошук блоку з картинкою
                parent = block.find_parent('div', class_='incr_loop-item')
                img_tag = parent.find('img') if parent else None
                image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else None

                articles.append({
                    'id_a': idx,
                    'title': article_title,
                    'link': article_url,
                    'image': image_url
                })

    return articles



def text_in_article(article):
    url = article['link'] if article else None
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Очистка підвалу
        for footer_element in soup.find_all('p', class_='footer-contacts-deskr'):
            footer_element.decompose()
        for doc_footer_element in soup.find_all('p', class_='documents-footer-title'):
            doc_footer_element.decompose()

        # Отримати текст
        paragraphs = soup.find_all('p')
        paragraph_texts = [p.text.strip() for p in paragraphs]

        # Імітація автора (реальний парсинг можна додати за потреби)
        fake_authors = ["CryptoCat", "ChainWriter", "BlockBee", "AnonX", "NakamotoJunior"]
        author = random.choice(fake_authors)

        return {
            'text': '\n'.join(paragraph_texts),
            'author': author
        }

    return {
        'text': "Текст не знайдено",
        'author': "Unknown"
    }


if __name__ == "__main__":
    list_of_articles()
    text_in_article()