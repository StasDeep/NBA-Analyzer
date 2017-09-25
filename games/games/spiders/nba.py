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
        teams = [x.split('/')[2] for x in response.css('.scorebox a[itemprop="name"]::attr(href)').extract()]
        datetime = response.css('.scorebox_meta div:first-child::text').extract_first()

        # Box scores tables (+ advanced).
        away_bs, away_bs_adv, home_bs, home_bs_adv = response.css('.stats_table tfoot')

        def away_stat(stat, to=int):
            return self.get_stat(away_bs, stat, to)

        def home_stat(stat, to=int):
            return self.get_stat(home_bs, stat, to)

        def team_stats(team):
            if team == 'away':
                get_stat = away_stat
            else:
                get_stat = home_stat

            stats = [
                'pts',
                'fg',
                'fga',
                'fg3',
                'fg3a',
                'ft',
                'fta',
                'orb',
                'drb',
                'ast',
                'stl',
                'blk',
                'tov',
                'pf',
            ]

            result = {stat_name: get_stat(stat_name) for stat_name in stats}
            result['team'] = teams[0] if team == 'away' else teams[1]

            return result

        yield {
            'away': team_stats('away'),
            'home': team_stats('home'),
            'datetime': datetime
        }

    def get_stat(self, box_score, stat, to):
        return to(box_score.css('td[data-stat="{}"]::text'.format(stat)).extract_first())
