import json


def get_all_films(file_path: str) -> list[dict]:
    with open(file_path, "r") as fd:
        films = json.load(fd)
        return films


def get_film(file_path: str, film_id: int):
    return get_all_films(file_path)[film_id]
