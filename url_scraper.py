# file that gets a url and scrapes the data from it
import pprint
import requests
from bs4 import BeautifulSoup

URLs = ["https://tv.nova.cz/porad/na-lovu/videa/cele-dily/strana-1", "https://tv.nova.cz/porad/na-lovu/videa/cele-dily/strana-2"]

# get html from url
def get_html(url):
    response = requests.get(url)
    return response.text

# find all class c-article
def get_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='c-article')
    return articles

# get data-tracking-tile-name from article and find an a tag
def parse_article(article):
    title = article['data-tracking-tile-name']
    order = title.split('.')[0]
    a = article.find('a')
    link = a['href']

    if 'voyo' in link:
        return

    return {
        'title': title,
        'link': link,
        'order': order
    }

# main method that combines all the functions
def get_episode_URLs():
    html = [get_html(url) for url in URLs]
    articles = [get_articles(page) for page in html]
    parsed_articles = [parse_article(article) for page in articles for article in page if parse_article(article)]

    if __name__ == "__main__":
        pprint.pprint(parsed_articles)

    return parsed_articles

if __name__ == "__main__":
    get_episode_URLs()
