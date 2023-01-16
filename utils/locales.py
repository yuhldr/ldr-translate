import copy
import json
import locale
import os

locale_data = None

locale_key_default = "zh_CN"
locale_dir = "./locales"

locale_file_default = "%s/%s.json" % (locale_dir, locale_key_default)


def get_locale_data(path_locale=locale_file_default):
    return json.load(open(path_locale, "r"))


def load_configs():
    global locale_data
    key = locale.getdefaultlocale()[0]
    path_locale = "%s/%s.json" % (locale_dir, key)
    if not os.path.exists(path_locale):
        path_locale = "%s/en_US.json" % locale_dir

    locale_data = get_locale_data(path_locale)


def t_translate(key):
    return t("translate.%s" % key)


def t_ui(key):
    return t("ui." + key)


# t(ldr.cl.sd)
def t(keys):
    if locale_data is None:
        load_configs()
    return t_(keys, locale_data)


def t_(keys, locale_data_):
    dicts = copy.deepcopy(locale_data_)
    for key in keys.split("."):
        if key in dicts:
            dicts = dicts[key]
        else:
            if locale_data["key"] == locale_key_default:
                return keys
            else:
                return t_(keys, get_locale_data())
    return dicts
