import peewee

db = peewee.SqliteDatabase('nba.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Team(BaseModel):
    id = peewee.CharField(max_length=3, primary_key=True)


class Game(BaseModel):
    date = peewee.DateField()


class Performance(BaseModel):
    HOME = 1
    AWAY = 2
    TYPES = [
        (HOME, 'Home'),
        (AWAY, 'Away')
    ]

    team = peewee.ForeignKeyField(Team, related_name='performances')
    game = peewee.ForeignKeyField(Game, related_name='performances')
    type = peewee.IntegerField(choices=TYPES)

    pts = peewee.IntegerField()   # Points
    fg = peewee.IntegerField()    # Shots from game made
    fga = peewee.IntegerField()   # Shots from game attempted
    fg3 = peewee.IntegerField()   # 3 pointers made
    fg3a = peewee.IntegerField()  # 3 pointers attempts
    ft = peewee.IntegerField()    # Free throws made
    fta = peewee.IntegerField()   # Free throws attempts
    orb = peewee.IntegerField()   # Offensive rebounds
    drb = peewee.IntegerField()   # Defensive rebounds
    ast = peewee.IntegerField()   # Assists
    stl = peewee.IntegerField()   # Steals
    blk = peewee.IntegerField()   # Blocks
    tov = peewee.IntegerField()   # Turnovers
    pf = peewee.IntegerField()    # Personal fouls
