from copy import deepcopy

from lol_dto.classes.game.lol_game import LolGame


class MergeError(Exception):
    pass


def merge_dicts(a, b, path=None):
    """Merges b into a recursively

    Returns:
        The a dictionary with b merged in it

    Raises:
        MergeError if a key present in the two dictionaries points to different values, except for lists
    """
    if path is None:  # Necessary because [] cannot be a default value
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                path.append(str(key))
                merge_dicts(a[key], b[key], path)
            elif isinstance(a[key], list) and isinstance(b[key], list):
                pass  # Lists fusing has to be handled case-by-case
            # In the case one is None/empty and the other is not, we use the non empty value
            elif not a and b:
                a[key] = b[key]
            elif not b and a:
                b[key] = a[key]
            elif a[key] == b[key]:
                pass  # Same leaf value, we pass
            else:
                path.append(str(key))
                raise MergeError(f"Conflict at {'.'.join(path)}\n" f"{a[key]} != {b[key]}")
        else:  # If the key isn’t in a, we just write the value from b
            a[key] = b[key]
    return a


def check_equal_field(field_name, dict_1, dict_2):
    if field_name in dict_1 and field_name in dict_2:
        try:
            assert dict_1[field_name] == dict_2[field_name]
        except AssertionError:
            raise MergeError(f"Conflict at {field_name}\n" f"{dict_1[field_name]} != {dict_2[field_name]}")


def merge_games(game_1: LolGame, game_2: LolGame) -> LolGame:
    """Merges two LolGame objects into a single one.

    If the two objects have similar keys, it will check their equality.

    Args:
        game_1: A LolGame
        game_2: A LolGame

    Returns:
        A LolGame

    Raises:
        MergeError if the two objects have incompatible data
    """
    # This merge will handle everything except lists
    output_game = merge_dicts(deepcopy(game_1), game_2)

    check_equal_field("kills", output_game, game_2)

    for team_side in output_game["teams"]:
        for field in ["bans", "monstersKills", "buildingsKills"]:
            check_equal_field(field, output_game, game_2)

        # Recreate players from scratch to control merging of the lists
        output_game["teams"][team_side]["players"] = []

        # Fuse g2 players into g1 players
        for g1_player in game_1["teams"][team_side]["players"]:
            try:
                # We try and match them on team side + champion ID
                try:
                    g2_player = next(
                        p for p in game_2["teams"][team_side]["players"] if p["championId"] == g1_player["championId"]
                    )
                # Sometimes we don’t have a championId, we then match on an "id" field
                except KeyError:
                    g2_player = next(p for p in game_2["teams"][team_side]["players"] if p["id"] == g1_player["id"])

            except StopIteration:
                raise MergeError("Conflict between player IDs")

            # Checking all list-based fields are equal or present in only one of the two objects
            for field in ["snapshots", "runes", "summonerSpells", "itemsEvents", "wardsEvents", "skillEvents"]:
                check_equal_field(field, g1_player, g2_player)

            # Basic merge that will check for similar values outside of lists
            new_player = merge_dicts(deepcopy(g1_player), g2_player)

            output_game["teams"][team_side]["players"].append(new_player)

    return output_game
