import requests
from bs4 import BeautifulSoup

WSR_URL = 'https://www.westsiderentals.com/apartments/westside-apartments/studio/'

def get_html_page(url):
    print(f'Requesting page {url}')
    r = requests.get(url)
    html_doc = r.text
    return html_doc

def get_pagination_count(soup):
    pagination_div = soup.find('div', class_='pagination')
    return int(pagination_div.span.next_sibling.text)

if __name__ == '__main__':
    html_doc = get_html_page(WSR_URL)
    soup = BeautifulSoup(html_doc, 'html.parser')
    pagination_count = get_pagination_count(soup)
