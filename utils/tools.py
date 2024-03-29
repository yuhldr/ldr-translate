from api import server_config
from utils import config
from utils.locales import t_translate

config_section = "setting"
last_translate_to_lang_cache = ""
translate_to_lang_cache = config.get_config_setting("translate_to_lang")

last_translate_server_cache = ""
translate_server_cache = config.get_config_setting("translate_server")


def get_value_by_dict(dict_, key):
    if key not in dict_:
        key = list(dict_.keys())[0]
    return dict_[key]


def get_translate_server_dict_by_locale():
    translate_server_dict = {}
    for translate_server in server_config.dict_to_lang.keys():
        key_ = t_translate("%s.name" % translate_server)
        translate_server_dict[key_] = translate_server

    return translate_server_dict


def get_translate_server_dict_by_code():
    server_dict = get_translate_server_dict_by_locale()
    return dict(zip(server_dict.values(), server_dict.keys()))


# 每次选择翻译服务，保存在本地
def set_translate_server(translate_server, by_code=False):
    global translate_server_cache
    if by_code:
        translate_server_cache = translate_server
    else:
        translate_server_cache = get_value_by_dict(
            get_translate_server_dict_by_locale(), translate_server)

    config.set_config(config_section, "translate_server",
                      translate_server_cache)


def get_current_translate_server_index():
    i = 0
    list_ = list(server_config.dict_to_lang.keys())
    if translate_server_cache in list_:
        i = list_.index(translate_server_cache)
    else:
        print("找不到", translate_server_cache)
    return i


def get_current_translate_server_code():
    return translate_server_cache


def get_current_translate_server_locale():
    return get_value_by_dict(get_translate_server_dict_by_code(),
                             translate_server_cache)


def get_current_translate_server(get_code=True):
    global last_translate_server_cache

    change_server = last_translate_server_cache != translate_server_cache

    last_translate_server_cache = translate_server_cache

    if get_code:
        s = get_current_translate_server_code()
    else:
        s = get_current_translate_server_locale()

    return s, change_server


# 通过多语言文字得到tolang的code
def get_to_lang_dict_by_locale():
    dict_to_langs = get_value_by_dict(server_config.dict_to_lang,
                                      translate_server_cache)
    to_langs_locale = {}

    for key in dict_to_langs:
        to_langs_locale[t_translate("to_lang.%s" % key)] = dict_to_langs[key]
    return to_langs_locale


# 通过code得到多语言文字
def get_to_lang_dict_by_code():
    to_langs_dict = get_to_lang_dict_by_locale()
    return dict(zip(to_langs_dict.values(), to_langs_dict.keys()))


# 最终保存的是要翻译的语言的简写编码，不同翻译服务略有不同
def set_to_lang(to_lang, by_code=False):
    if to_lang is None:
        return
    global translate_to_lang_cache
    if not by_code:
        translate_to_lang_cache = get_value_by_dict(
            get_to_lang_dict_by_locale(), to_lang)
    else:
        translate_to_lang_cache = to_lang

    config.set_config(config_section, "translate_to_lang",
                      translate_to_lang_cache)


def get_current_to_lang_index(translate_to_lang=translate_to_lang_cache):
    i = 0
    list_ = list(get_to_lang_dict_by_locale().values())
    if translate_to_lang in list_:
        i = list_.index(translate_to_lang)
    else:
        print("找不到", translate_to_lang, list_)
    return i


def get_current_to_lang_code():
    return translate_to_lang_cache


def get_current_to_lang_locale():
    return get_value_by_dict(get_to_lang_dict_by_code(),
                             translate_to_lang_cache)


def get_current_to_lang(get_code=True):
    global last_translate_to_lang_cache

    change_language = last_translate_to_lang_cache != translate_to_lang_cache

    last_translate_to_lang_cache = translate_to_lang_cache

    s = translate_to_lang_cache

    if get_code:
        s = get_current_to_lang_code()
    else:
        s = get_current_to_lang_locale()

    return s, change_language


def error2zh(error_code,
             error_msg,
             dict_,
             server=get_current_translate_server_code()):
    print(error_code, error_msg)
    error_code = str(error_code)
    s = ""
    if error_code in dict_:
        s = dict_[error_code]

    s = t_translate("%s.%s" % (server, s))

    s = "%s\n\n%s，%s" % (s, error_code, error_msg)

    return s.strip()
