import luigi
from scrapy.crawler import CrawlerProcess

from games_spider import GamesSpider


class Games(luigi.Task):
    season = luigi.IntParameter(default=2017)

    def run(self):
        process = CrawlerProcess()
        process.crawl(GamesSpider, season=self.season, feed_uri=self.output().path)
        process.start()

    def output(self):
        return luigi.LocalTarget('data/games_{}.csv'.format(self.season))


if __name__ == '__main__':
    luigi.run()
