import re
import unicodedata
from collections import defaultdict

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

def get_placard_links(soup):
    placard_links = soup.find_all('a',
                                  href= re.compile(r'ca'),
                                  class_= lambda x: x and x.startswith('placard'))
    placard_links = [l for l in placard_links if not l.findChild()]
    return placard_links

def map_placard_links(placard_links):
    link_dict = defaultdict(dict)
    for l in placard_links:
        record = { l['class'][0]: unicodedata.normalize('NFKD', l.get_text(strip=True)) }
        link_dict[l['href']].update(record)
    return link_dict

if __name__ == '__main__':
    html_doc = get_html_page(WSR_URL)
    soup = BeautifulSoup(html_doc, 'html.parser')

    pagination_count = get_pagination_count(soup)
    print(f'Found {pagination_count} pages of results')

    placard_links = get_placard_links(soup)
    link_dict = map_placard_links(placard_links)
