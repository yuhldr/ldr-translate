import os
from api.server import baidu
import time
from api import config

last_s = ""
last_s2 = "空白"
last_time = 0

path_next_s = "s_next"
config_section = "setting"

# 整合一下，方便接入其他api接口


def text(s_from, fromLang="auto", type="baidu", add_old=True):
    global last_s, last_s2, last_time
    toLang, changeLang = get_to_language()
    config_setting = config.get_config_section(config_section)

    translate_span = config_setting["translate_span"]

    # 文字和上次一样，并且被翻译的语言没有修改，就不翻译了
    if (last_s == s_from and not changeLang):
        return last_s, last_s2
    span = translate_span * 1.2 - (time.time() - last_time)
    if (span > 0):
        time.sleep(span)
    if (add_old):
        s_from = last_s + " " + s_from

    if (type == "baidu"):
        last_s2 = baidu.translate_text(s_from, fromLang, toLang)
    else:
        last_s2 = baidu.translate_text(s_from, fromLang, toLang)

    last_s = s_from
    last_time = time.time()
    return last_s, last_s2


def ocr(img, type="baidu"):

    if (type == "baidu"):
        s = baidu.ocr(img)
    else:
        s = baidu.ocr(img)

    return s


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
    i = translate_to_languages_zh.index(zh)
    if (i < 0):
        i = 0
    return i


def check_server_translate(server, a, b):
    ok = False
    if (server == "baidu"):
        ok = baidu.check_translate(a, b)
    else:
        ok = baidu.check_translate(a, b)

    return ok


def check_server_ocr(server, a, b):
    ok = False

    if (server == "baidu"):
        ok = baidu.check_ocr(a, b)
    else:
        ok = baidu.check_ocr(a, b)

    return ok
