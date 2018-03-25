import luigi
from scrapy.crawler import CrawlerProcess

from games_spider import GamesSpider
from prepare import prepare_data_for_train


class ScrapedGames(luigi.Task):
    season = luigi.IntParameter(default=2017)

    def run(self):
        process = CrawlerProcess()
        process.crawl(GamesSpider, season=self.season, feed_uri=self.output().path)
        process.start()

    def output(self):
        return luigi.LocalTarget('data/games_{}.csv'.format(self.season))


class PreparedGames(luigi.Task):
    season = luigi.IntParameter(default=2017)

    def requires(self):
        return ScrapedGames(self.season)

    def run(self):
        data = prepare_data_for_train(self.input().path)

        with self.output().open('w') as outfile:
            outfile.write(data)

    def output(self):
        return luigi.LocalTarget('data/train_{}.csv'.format(self.season))


class AllGames(luigi.Task):

    def requires(self):
        return [PreparedGames(season) for season in range(2000, 2018)]


if __name__ == '__main__':
    luigi.run()
