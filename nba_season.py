import requests
from bs4 import BeautifulSoup


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
        self.game_links = []

        self.load_months()

    def load_months(self):
        for month in self.months:
            url = self.url_template.format(self.year, month)
            self.load_month(url)

    def load_month(self, url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('#schedule tbody tr')

        for row in rows:
            try:
                self.game_links.append(row.find_all('td')[5].find('a')['href'])
            except IndexError:
                # *Playoffs* row does not have 'td' tags inside.
                break
