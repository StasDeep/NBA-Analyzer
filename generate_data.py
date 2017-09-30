#!/usr/bin/python3

from csv import writer
from datetime import datetime, timedelta

from models import Team, Performance, Game


STATS = [
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


def get_games():
    return Game.select().where(Game.date > datetime(2015, 8, 1))


def get_team_avg_performance(team_id, to_date):
    from_date = to_date - timedelta(days=21)

    query = (Performance
             .select()
             .join(Game)
             .switch(Performance)
             .join(Team)
             .where(Team.id == team_id,
                    Game.date >= from_date,
                    Game.date < to_date))

    count = query.count()
    if count < 5:
        return

    features = [0 for _ in STATS]

    for perf in query:
        for i, stat in enumerate(STATS):
            features[i] += getattr(perf, stat)

    features = [f // count for f in features]

    return features


def get_pregame_info(game):
    home_perf, away_perf = game.performances

    if home_perf.type != Performance.HOME:
        home_perf, away_perf = away_perf, home_perf

    total_points = home_perf.pts + away_perf.pts

    print(game.date.strftime('%Y.%m.%d'))
    print('{} {}:{} {} ({} total)'.format(home_perf.team_id,
                                          home_perf.pts,
                                          away_perf.pts,
                                          away_perf.team_id,
                                          total_points))

    home_avg = get_team_avg_performance(home_perf.team_id, game.date)
    if home_avg is None:
        return

    away_avg = get_team_avg_performance(away_perf.team_id, game.date)
    if away_avg is None:
        return

    return home_avg + away_avg + [total_points]


def write_to_csv(data):
    with open('training.csv', 'w', newline='') as csvfile:
        csvwriter = writer(csvfile)
        for row in data:
            csvwriter.writerow(row)


def main():
    training_set = []

    for game in get_games():
        example = get_pregame_info(game)

        if example is not None:
            training_set.append(example)

    write_to_csv(training_set)


if __name__ == '__main__':
    main()
