#!/usr/bin/python3

from models import Team, Performance, Game, db


def main():
    db.connect()
    db.create_tables([Team, Performance, Game])


if __name__ == '__main__':
    main()

