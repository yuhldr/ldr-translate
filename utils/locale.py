import json
import copy

locale_data = None


def load_configs():
    global locale_data
    locale_key = "zh"
    path_locale = "locales/%s.json" % locale_key
    with open(path_locale, "r") as file:
        locale_data = json.load(file)


def t_translate(key):
    return t("translate.%s" % key)


def t_ui(key):
    return t("ui." + key)


# t(ldr.cl.sd)
def t(keys):
    if (locale_data is None):
        load_configs()
    dicts = copy.deepcopy(locale_data)
    for key in keys.split("."):
        if(key in dicts):
            dicts = dicts[key]
        else:
            return keys
    return dicts
