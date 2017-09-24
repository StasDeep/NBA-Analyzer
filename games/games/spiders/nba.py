# -*- coding: utf-8 -*-
import scrapy


class NbaSpider(scrapy.Spider):
    name = 'nba'
    season_template = 'https://www.basketball-reference.com/leagues/NBA_{}_games.html'

    def start_requests(self):
        year = int(getattr(self, 'year', '2017'))
        url = self.season_template.format(year)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for a_tag in response.css('.filter a'):
            yield response.follow(a_tag, callback=self.parse_month)

    def parse_month(self, response):
        for a_tag in response.css('.stats_table tbody tr td:nth-child(7) a'):
            yield response.follow(a_tag, callback=self.parse_game)

    def parse_game(self, response):
        scores = [int(x) for x in response.css('.scorebox .score::text').extract()]
        teams = response.css('.scorebox a[itemprop="name"]::text').extract()
        yield {
            'home_team': {
                'name': teams[0],
                'score': scores[0]
            },
            'guest_team': {
                'name': teams[1],
                'score': scores[0]
            }
        }
