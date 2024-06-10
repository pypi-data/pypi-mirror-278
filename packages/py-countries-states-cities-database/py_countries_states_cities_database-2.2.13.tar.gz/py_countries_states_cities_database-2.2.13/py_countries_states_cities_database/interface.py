import os
import json

# all country info
from pkg_resources import resource_filename


def get_all_cities():
    with open(
        resource_filename(__name__, "cities.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states():
    with open(
        resource_filename(__name__, "states.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries():
    with open(
        resource_filename(__name__, "countries.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_sub_regions():
    with open(
        resource_filename(__name__, "subregions.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_regions():
    with open(
        resource_filename(__name__, "regions.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_cities_nested():
    with open(
        resource_filename(__name__, "countries+cities.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_and_states_nested():
    with open(
        resource_filename(__name__, "countries+states.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_states_and_cities_nested():
    with open(
        resource_filename(__name__, "states+cities.json"),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_all_countries_states_and_cities_nested():
    with open(
        resource_filename(
            __name__,
            "countries+states+cities.json",
        ),
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_file_path(file_name):
    return resource_filename(__name__, file_name)
