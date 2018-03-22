import scrapy

from constants import STATS_NAMES


class GamesSpider(scrapy.Spider):
    name = 'nba'
    download_delay = 1
    season_template = 'https://www.basketball-reference.com/leagues/NBA_{}_games.html'
    custom_settings = {
        'FEED_URI': '%(feed_uri)s',
        'FEED_FORMAT': 'csv'
    }

    def start_requests(self):
        url = self.season_template.format(self.season)
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for a_tag in response.css('.filter a'):
            yield response.follow(a_tag, callback=self.parse_month)

    def parse_month(self, response):
        for a_tag in response.css('.stats_table tbody tr td:nth-child(7) a'):
            yield response.follow(a_tag, callback=self.parse_game)

    def parse_game(self, response):
        game_id = response.request.url.split('/')[-1][:-5]
        date = response.css('.scorebox_meta div:first-child::text').extract_first().split(', ')[1]

        away_bs, _, home_bs, _ = response.css('.stats_table tbody')

        for box_score, is_home in [(home_bs, True), (away_bs, False)]:
            player_rows = box_score.css('tr:not(.thead)')

            for prow in player_rows:
                performance = {
                    'game_id': game_id,
                    'date': date,
                    'is_home': is_home,
                    'player_id': prow.css('a::attr(href)').extract_first().split('/')[-1][:-5]
                }

                # Check if player had a reason not to play
                if prow.css('td[data-stat="reason"]'):
                    for stat_name in STATS_NAMES:
                        performance[stat_name] = 0
                else:
                    for stat_name in STATS_NAMES:
                        if stat_name == 'mp':
                            performance[stat_name] = int(self.get_stat(prow, 'mp', str).split(':')[0])
                        else:
                            performance[stat_name] = self.get_stat(prow, stat_name)

                yield performance

    def get_stat(self, prow, stat, stat_type=int):
        return stat_type(prow.css('td[data-stat="{}"]::text'.format(stat)).extract_first())
