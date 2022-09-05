import re
from api.server import baidu, tencent, youdao, google
import time
from utils import tools, config
from api import server_config
from utils.locale import get_locale_ui_data as locale_ui

last_s = None
last_s2 = None
last_time = 0

no_translate_this = False

path_next_s = "s_next"
config_section = "setting"

# 整合一下，方便接入其他api接口


def text(s_from, add_old=True):
    global last_s, last_s2, last_time, no_translate_this

    if (no_translate_this):
        print("不翻译")
        no_translate_this = False
        return "", ""

    to_lang_code, changeLang = tools.get_current_to_lang()
    server, changeServer = tools.get_current_translate_server()

    translate_span = config.get_config_setting("translate_span")

    if (s_from is None):
        if (last_s is None):
            return locale_ui("notice_from"), locale_ui("notice_to")
        else:
            s_from = last_s

    # 文字和上次一样，并且被翻译的语言没有修改，就不翻译了
    if (last_s == s_from and not changeLang and not changeServer):
        return last_s, last_s2
    span = translate_span * 1.2 - (time.time() - last_time)
    if (span > 0):
        time.sleep(span)

    if (add_old):
        s_from = last_s + " " + s_from

    s_from = re.sub(r"-[\n|\r]+", "", s_from)
    s_from = re.sub(r"(?<!\.|-|。)[\n|\r]+", " ", s_from)

    last_s2 = translate(s_from, server, to_lang_code)

    last_s = s_from
    last_time = time.time()
    return last_s, last_s2


def translate(s, server, to_lang_code, fromLang="auto"):

    if (server == server_config.server_tencent):
        s = tencent.translate_text(s, fromLang, to_lang_code)
    elif (server == server_config.server_baidu):
        s = baidu.translate_text(s, fromLang, to_lang_code)
    elif (server == server_config.server_youdao):
        s = youdao.translate_text(s, fromLang, to_lang_code)
    else:
        s = google.translate_text(s, fromLang, to_lang_code)

    return s


def ocr(img_path, latex=False):

    server, changeServer = tools.get_current_translate_server()
    if (server == server_config.server_tencent):
        # 这个有问题，暂时用百度的
        # ok, s = tencent.ocr(img_path, latex=latex)
        ok, s = baidu.ocr(img_path, latex=latex)
    else:
        ok, s = baidu.ocr(img_path, latex=latex)

    return ok, s


def check_server_translate(server, a, b):
    ok = False
    a = a.strip().replace("\n", " ")
    b = b.strip().replace("\n", " ")

    if (server == server_config.server_tencent):
        ok = tencent.check(a, b)
    else:
        ok = baidu.check_translate(a, b)

    return ok, a, b


def check_server_ocr(server, a, b):
    ok = False
    a = a.strip().replace("\n", " ")
    b = b.strip().replace("\n", " ")

    if (server == server_config.server_tencent):
        ok = tencent.check(a, b)
    else:
        ok = baidu.check_ocr(a, b)
    print(ok, a, b)
    return ok, a, b


def set_no_translate_this(ntt=True):
    global no_translate_this
    no_translate_this = ntt
