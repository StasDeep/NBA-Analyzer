import peewee

db = peewee.SqliteDatabase('nba.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Season(BaseModel):
    year = peewee.IntegerField()


class Team(BaseModel):
    id = peewee.CharField(max_length=3, primary_key=True)


class Performance(BaseModel):
    team = peewee.ForeignKeyField(Team, related_name='performances')
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


class Game(BaseModel):
    home_performance = peewee.ForeignKeyField(Performance)
    away_performance = peewee.ForeignKeyField(Performance)
    date = peewee.DateField()
