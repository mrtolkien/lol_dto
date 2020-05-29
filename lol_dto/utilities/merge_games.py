from copy import deepcopy

from lol_dto.classes.game.lol_game import LolGame


class MergeError(Exception):
    pass


def merge_dicts(a, b, path=None):
    """Merges b into a"""
    if path is None:  # Necessary because [] cannot be a default value
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                path.append(str(key))
                merge_dicts(a[key], b[key], path)
            elif isinstance(a[key], list) and isinstance(b[key], list):
                pass  # Lists fusing has to be handled case-by-case
            elif a[key] == b[key]:
                pass  # Same leaf value
            else:
                path.append(str(key))
                raise MergeError(f"Conflict at {'.'.join(path)}")
        else:
            a[key] = b[key]
    return a


def merge_games(game_1: LolGame, game_2: LolGame) -> LolGame:
    """Merges two LolGame objects into a single one.

    Args:
        game_1: A LolGame
        game_2: A LolGame

    Returns:
        A LolGame

    Raises:
        MergeError if the two objects have incompatible data.
    """
    output_game = deepcopy(game_1)
    output_game = merge_dicts(output_game, game_2)

    # If events is present in only one of them, it will already have been handled
    if "events" in game_1 and "events" in game_2:
        output_game["events"] += game_2["events"]
        output_game["events"] = sorted(output_game["events"], key=lambda x: x["timestamp"])

    for team_side in output_game['teams']:
        # If both objects had bans already filled, assert they are equal
        if "bans" in output_game['teams'][team_side] and "bans" in game_2['teams'][team_side]:
            try:
                assert output_game['teams'][team_side]['bans'] == game_2['teams'][team_side]['bans']
            except AssertionError:
                raise MergeError("Conflict at game.teams.bans")

        # Recreate players from scratch to control merging of the lists
        output_game['teams'][team_side]['players'] = []

        # Fuse g2 players into g1 players
        for g1_player in game_1['teams'][team_side]['players']:
            new_player = deepcopy(g1_player)

            try:
                g2_player = next(p for p in game_2['teams'][team_side]['players'] if p['id'] == g1_player['id'])
            except StopIteration:
                raise MergeError("Conflict between player IDs")

            # Basic merge that will check for similar values outside of snapshots
            # If snapshots are present in only one of the two games, they’re automatically merged
            new_player = merge_dicts(new_player, g2_player)

            # If both objects have snapshots, we merge them, without caring for timestamps at the moment
            if 'snapshots' in g1_player and 'snapshots' in g2_player:
                # We create dictionaries keyed on timestamps to merge data simply
                g1_snapshots_dict = {s['timestamp']: s for s in g1_player['snapshots']}
                g2_snapshots_dict = {s['timestamp']: s for s in g2_player['snapshots']}

                full_snapshots = merge_dicts(g1_snapshots_dict, g2_snapshots_dict)

                new_player['snapshots'] = sorted(list(full_snapshots.values()), key=lambda x: x['timestamp'])

            output_game['teams'][team_side]['players'].append(new_player)

    return output_game
