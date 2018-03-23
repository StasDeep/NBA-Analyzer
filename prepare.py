import pandas as pd


def prepare_data_for_train(filename):
    df = pd.read_csv(filename)

    game_ids = df['game_id'].unique()

    pregame_data = []
    for game_id in game_ids:
        game_players = df[df['game_id'] == game_id]
        player_ids = game_players['player_id']
        players_df = pd.DataFrame()

        skip = False

        for player_id in player_ids:
            previous_games = df[(df['player_id'] == player_id) & (df['game_id'] < game_id)].sort_values('game_id')
            prev_five_games = previous_games.iloc[-5:]

            if len(prev_five_games) < 5:
                skip = True
                break

            for prev_game_id in prev_five_games['game_id']:
                performance = prev_five_games[
                    (prev_five_games['game_id'] == prev_game_id) & (prev_five_games['player_id'] == player_id)]
                performance = performance.assign(
                    is_home_now=game_players[game_players['player_id'] == player_id]['is_home'].astype(int).values)
                players_df = players_df.append(performance[['game_id', 'player_id', 'pts', 'is_home', 'is_home_now']])

        if skip:
            print('SKIPPED GAME {} DUE TO {} HAS PLAYED IN {} GAMES'.format(game_id, player_id, len(prev_five_games)))
            continue

        players_df['is_home'] = players_df['is_home'].astype(int)
        pregame_data.extend(players_df.to_csv(None, index=False).split('\n')[1:-1])
        total_points = game_players['pts'].sum()
        pregame_data.append('{},{}'.format(game_id, total_points))
        pregame_data.append('=')

        print('PREPARED GAME {}'.format(game_id))

    return '\n'.join(pregame_data)
