import requests

class NbaSeason:

    url_template = 'https://basketball-reference.com/leagues/NBA_{}_games-{}.html'
    months = (
        'october',
        'november',
        'december',
        'january',
        'february',
        'march',
        'april'  # TODO: search for playoffs row
    )

    def __init__(self, year):
        self.year = year

        self.load_months()

    def load_months(self):
        for month in self.months:
            url = self.url_template.format(self.year)
            self.load_month(url)

    def load_month(self, url):
        response = requests.get(url)
