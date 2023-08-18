import requests
from bs4 import BeautifulSoup
import json

# Скрапінг сайту та збереження даних
def scrape_quotes():
    quotes_data = []
    authors_data = []

    base_url = 'http://quotes.toscrape.com'
    page_number = 1
    while True:
        print(page_number)
        url = f'{base_url}/page/{page_number}/'
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            break

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            quotes_data.append({
                'quote': text,
                'author': author,
                'tags': tags
            })

            author_url = quote.find('small', class_='author').find_next('a', href=True)['href']
            author_response = requests.get(f'{base_url}{author_url}')
            author_soup = BeautifulSoup(author_response.content, 'html.parser')
            born_date = author_soup.find('span', class_='author-born-date').text
            born_location = author_soup.find('span', class_='author-born-location').text
            description = author_soup.find('div', class_='author-description').text.strip()

            authors_data.append({
                'fullname': author,
                'born_date': born_date,
                'born_location': born_location,
                'description': description
            })

        page_number += 1


    with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=4)

    with open('authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(authors_data, authors_file, ensure_ascii=False, indent=4)

# Виклик функції для скрапінгу та збереження даних
scrape_quotes()
