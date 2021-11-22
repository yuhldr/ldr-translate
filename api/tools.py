from api import config

config_section = "setting"
to_language_zh = ""
last_to_language_zh = ""
translate_to_languages_zh = config.get_config_setting(
)["translate_to_languages_zh"]


def set_to_language(to_lg):
    global to_language_zh
    to_language_zh = to_lg
    config.set_config(config_section, "to_long", to_lg)


def get_to_language():
    global to_language_zh, last_to_language_zh

    change_language = last_to_language_zh != to_language_zh

    to_language_zh = config.get_config_setting()["to_long"]
    last_to_language_zh = to_language_zh

    return to_language_zh, change_language


# 中文转为序号，与第三方对应
def zh2LangPar(zh):
    if(zh is None or len(zh) == 0):
        return 0
    i = translate_to_languages_zh.index(zh)
    if (i < 0):
        i = 0
    return i
