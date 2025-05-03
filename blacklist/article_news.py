import requests
from bs4 import BeautifulSoup
import re

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
                articles.append({
                    'id_a': idx,
                    'title': a_tag.text.strip(),
                    'link': a_tag['href'].strip()
                })

    return articles



def text_in_article(article):
    url = article['link'] if article else None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')


        footer_elements = soup.find_all('p', class_='footer-contacts-deskr')
        for footer_element in footer_elements:
            footer_element.decompose()

        documents_footer_elements = soup.find_all('p', class_='documents-footer-title')
        for doc_footer_element in documents_footer_elements:
            doc_footer_element.decompose()


        paragraphs = soup.find_all('p')

        paragraph_texts = [p.text.strip() for p in paragraphs]



        return '\n'.join(paragraph_texts)

    return "Текст не знайдено"


if __name__ == "__main__":
    list_of_articles()
    text_in_article()