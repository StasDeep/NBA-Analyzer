from datetime import datetime
from json import load
from sys import argv

from models import Team, Performance, Game


def get_games():
    with open(argv[1]) as infile:
        data = load(infile)

    return data


def commit_games(games):
    for game in games:
        home = game['home']
        away = game['away']

        Team.get_or_create(id=home['team'])
        Team.get_or_create(id=away['team'])

        home_performance = Performance.create(**home)
        away_performance = Performance.create(**away)
        date_string = game['datetime'].split(',', 1)[1].strip()
        date = datetime.strptime(date_string, '%B %d, %Y')

        Game.create(
            home_performance=home_performance,
            away_performance=away_performance,
            date=date
        )


def main():
    games = get_games()
    commit_games(games)


if __name__ == '__main__':
    main()
