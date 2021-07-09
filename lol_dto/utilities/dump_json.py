import json
import dataclasses
from typing import Union

from lol_dto.classes.game import LolGame


def dump_json(
    lol_game: Union[LolGame, dataclasses.dataclass],
    filename: str,
    remove_empty: bool = True,
):
    """
    Dump the given LolGame to a local file in JSON format

    Args:
        lol_game: the LolGame object to dump or a similar dataclass
        filename: the file to dump to
        remove_empty: whether or not to dump None fields in the JSON. True by default to heavily lighten the object

    Returns:
        Nothing

    """

    output_dict = dataclasses.asdict(lol_game)

    if remove_empty:
        output_dict = delete_empty_fields(output_dict)

    with open(filename, "w+") as file:
        json.dump(output_dict, file)


def delete_empty_fields(d: dict) -> dict:
    """
    Deletes the None fields in a dictionary recursively
    Mostly used to make resulting JSON dumps lighter

    Args:
        d: The dictionary to reduce

    Returns:
        The reduced dictionary

    """
    for key, value in list(d.items()):
        if isinstance(value, dict):
            delete_empty_fields(value)
        elif value is None:
            d.pop(key)
        elif isinstance(value, list):
            for list_value in value:
                if isinstance(list_value, dict):
                    delete_empty_fields(list_value)

    return d
