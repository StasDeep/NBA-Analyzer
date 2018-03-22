import pandas as pd


def clean(df):
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')
    game_ids = df['game_id'].unique()
    for game_id in game_ids[4:5]:
        game_players = df[df['game_id'] == game_id]
        player_ids = game_players['player_id']
        for player_id in player_ids:
            previous_games = df[(df['player_id'] == player_id) & (df['game_id'] < game_id)]
            print(len(previous_games['game_id']))

        return df
