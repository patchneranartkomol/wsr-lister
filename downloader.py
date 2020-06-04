import csv
import re
import unicodedata
from collections import defaultdict
from datetime import date

import requests
from bs4 import BeautifulSoup

WSR_URL = 'https://www.westsiderentals.com/apartments/westside-apartments/studio/'

def get_html_page(url):
    print(f'Requesting page {url}')
    r = requests.get(url)
    html_doc = r.text
    return html_doc

def format_wsr_url(page_number):
    return WSR_URL + f'page-{page_number}'

def get_pagination_count(soup):
    pagination_div = soup.find('div', class_='pagination')
    return int(pagination_div.span.next_sibling.text)

def get_placard_links(soup):
    placard_links = soup.find_all('a',
                                  href= re.compile(r'ca'),
                                  class_= lambda x: x and x.startswith('placard'))
    placard_links = [l for l in placard_links if not l.findChild()]
    return placard_links

def map_placard_links(placard_links, link_dict):
    for l in placard_links:
        class_ = l['class'][0]
        value = l.get_text(strip=True)
        if class_ == 'placardLocation':
            value = unicodedata.normalize('NFKD', value)
        record = { class_ : value }
        link_dict[l['href']].update(record)

def write_csv(link_dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['placardHeader', 'placardLocation', 'placardPrice']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for key, record_dict in link_dict.items():
            writer.writerow(record_dict)


if __name__ == '__main__':
    html_doc = get_html_page(WSR_URL)
    soup = BeautifulSoup(html_doc, 'html.parser')

    pagination_count = get_pagination_count(soup)
    print(f'Found {pagination_count} pages of results')

    link_dict = defaultdict(dict)
    placard_links = get_placard_links(soup)
    map_placard_links(placard_links, link_dict)

    if pagination_count > 1:
        for i in range(2, pagination_count + 1):
            page_url = format_wsr_url(i)
            html_doc = get_html_page(page_url)
            soup = BeautifulSoup(html_doc, 'html.parser')
            placard_links = get_placard_links(soup)
            map_placard_links(placard_links, link_dict)

    print('Writing results to CSV')
    today = date.today()
    filename = f"{today.strftime('%b-%d-%Y')}_wsr.csv"

    write_csv(link_dict, filename)
