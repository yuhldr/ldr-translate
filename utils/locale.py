import json

locale_data = None


def load_configs():
    global locale_data
    locale_key = "zh"
    path_locale = "locales/%s.json" % locale_key
    with open(path_locale, "r") as file:
        locale_data = json.load(file)


def get_locale_data(section, key):
    if (locale_data is None):
        load_configs()
    return locale_data[section][key]


def get_locale_translate_data(section, key):
    return get_locale_data("translate", section)[key]


def get_locale_ui_data(key):
    return get_locale_data("ui", key)
