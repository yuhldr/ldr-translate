import re
from api.server import baidu
import time
from api import config, tools

last_s = None
last_s2 = None
last_time = 0

path_next_s = "s_next"
config_section = "setting"

# 整合一下，方便接入其他api接口


def text(s_from, fromLang="auto", type="baidu", add_old=True):
    global last_s, last_s2, last_time
    toLang, changeLang = tools.get_to_language()
    config_setting = config.get_config_section(config_section)

    translate_span = config_setting["translate_span"]

    if(s_from is None):
        if(last_s is None):
            return "复制即可翻译", "系统直接截图到剪贴板，自动识别并翻译" + "\n\n测试功能：\n勾选latex识别，可将图片公式转化为latex代码"
        else:
            s_from = last_s

    # 文字和上次一样，并且被翻译的语言没有修改，就不翻译了
    if (last_s == s_from and not changeLang):
        return last_s, last_s2
    span = translate_span * 1.2 - (time.time() - last_time)
    if (span > 0):
        time.sleep(span)
    if (add_old):
        s_from = last_s + " " + s_from

    s_from = s_from.replace("-\n", "").strip()
    s_from = re.sub("(?<!\.|-|。)\n", " ", s_from)

    if (type == "baidu"):
        last_s2 = baidu.translate_text(s_from, fromLang, toLang)
    else:
        last_s2 = baidu.translate_text(s_from, fromLang, toLang)

    last_s = s_from
    last_time = time.time()
    return last_s, last_s2


def ocr(img, type="baidu", latex=False):

    if (type == "baidu"):
        s = baidu.ocr(img, latex=latex)
    else:
        s = baidu.ocr(img, latex=latex)

    return s


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
