from datetime import datetime
from json import load
from sys import argv
from argparse import ArgumentParser

from models import Team, Performance, Game


def get_filenames():
    parser = ArgumentParser(description='Load games to DB')
    parser.add_argument('files', metavar='FILE', nargs='+', help='JSON fies with games info')

    return parser.parse_args().files


def get_games(filenames):
    games = []

    for filename in filenames:
        with open(filename) as infile:
            data = load(infile)
            games.extend(data)

    return games


def commit_games(games):
    for game in games:
        home = game['home']
        away = game['away']

        Team.get_or_create(id=home['team'])
        Team.get_or_create(id=away['team'])

        date_string = game['datetime'].split(',', 1)[1].strip()
        date = datetime.strptime(date_string, '%B %d, %Y')
        game = Game.create(date=date)

        home['game_id'] = game.id
        away['game_id'] = game.id

        home['type'] = Performance.HOME
        away['type'] = Performance.AWAY

        Performance.create(**home)
        Performance.create(**away)


def main():
    filenames = get_filenames()
    games = get_games(filenames)
    commit_games(games)


if __name__ == '__main__':
    main()
