# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import scrapy

"""
To run: `scrapy crawl shackleton`

Extracts transcripts of Endurance's quartermaster's
journal from Dartmouth Library's Rauner Special Collections
and saves results to file.

also of note: https://www.pbs.org/wgbh/nova/shackleton/1914/diary.html
"""


class ShackletonSpider(scrapy.Spider):
    name = 'shackleton'
    attribution = 'By Thomas Orde-Lees, Quartermaster'
    filename = 'ThomasOrdesLees_journal.txt'
    start_urls = [
        'https://sites.dartmouth.edu/library/2016/07/12/shackletons-endurance-expedition-a-crewmans-view-2/'
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        article = soup.find_all('div', class_='entry-content')[0]

        for child in article.contents:
            # We're only interested in <p> tags
            if child.name != 'p':
                continue

            # Stop at pagination links
            if self.is_pagination_links(child):
                next_link = self.parse_next_url(child)
                if next_link is None:
                    return
                else:
                    yield scrapy.Request(next_link, callback=self.parse)
                    return

            # Append to file
            # if len(child.contents) == 1:
            text = child.text.strip('"')
            # import pdb; pdb.set_trace()
            if text in {self.attribution, ' ', '&nbsp;', '\xa0'}:
                continue
            with open(self.filename, 'a+') as f:
                f.write(text + '\n')

    def parse_next_url(self, paragraph_tag):
        for child in paragraph_tag.contents:
            if child.name == 'a' and child.text.startswith('Next entry'):
                next_link = self.normalize_url(child.get('href'))
                return next_link

    @staticmethod
    def is_pagination_links(paragraph_tag):
        for child in paragraph_tag.contents:
            if child.name != 'a':
                continue
            if child.text.startswith('Next entry'):
                return True
            if child.text.startswith('Previous entry'):
                return True

    @staticmethod
    def normalize_url(url):
        if not url.startswith('http'):
            url = 'http://{}'.format(url)
        return url
