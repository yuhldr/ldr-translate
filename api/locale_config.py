import json
from api import config

locale_data = None


def load_configs():
    global locale_data
    locale_data = json.load(open(config.config_locale_home_path, "r"))


def get_locale_data(section, key):
    if (locale_data is None):
        load_configs()
    locale_key = "zh"
    return locale_data[locale_key][section][key]


def get_locale_translate_data(section, key):
    return get_locale_data("translate", section)[key]


def get_locale_ui_data(key):
    return get_locale_data("ui", key)
