import json
from json.decoder import JSONDecodeError


def get_all_films(file_path: str) -> list[dict]:
    try:
        with open(file_path, "r") as fd:
            films = json.load(fd)
            return films
    except JSONDecodeError as e:
        return


def get_film(file_path: str, film_id: int):
    return get_all_films(file_path)[film_id]


def add_film(file_path: str, data_film: dict):

    films = get_all_films(file_path)
    if not films:
        films = []

    films.append(data_film)

    with open(file_path, "w") as fd:
        json.dump( films, fd, indent=4, ensure_ascii=False)
