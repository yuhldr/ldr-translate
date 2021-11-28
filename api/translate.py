import re
from api.server import baidu, tencent
import time
from api import config, tools

last_s = None
last_s2 = None
last_time = 0

path_next_s = "s_next"
config_section = "setting"

# 整合一下，方便接入其他api接口


def text(s_from, fromLang="auto", add_old=True):
    global last_s, last_s2, last_time
    toLangZh, changeLang = tools.get_to_lang_zh_()

    server, changeServer = tools.get_server_()

    config_setting = config.get_config_section(config_section)

    translate_span = config_setting["translate_span"]

    if (s_from is None):
        if (last_s is None):
            return "复制即可翻译", "系统直接截图到剪贴板，自动识别并翻译" + "\n\n测试功能：\n勾选latex识别，可将图片公式转化为latex代码"
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
    s_from = s_from.replace("-\n", "").strip()
    s_from = re.sub("(?<!\.|-|。)\n", " ", s_from)

    last_s2 = translate(s_from, toLangZh, server, fromLang)

    last_s = s_from
    last_time = time.time()
    return last_s, last_s2


def translate(s, toLangZh, server, fromLang="auto"):

    if (server == tools.server_tencent):
        s = tencent.translate_text(s, fromLang, toLangZh)
    else:
        s = baidu.translate_text(s, fromLang, toLangZh)

    return s


def ocr(img_path, latex=False):

    if (tools.get_server() == tools.server_tencent):
        # 这个有问题，暂时用百度的
        # ok, s = tencent.ocr(img_path, latex=latex)
        ok, s = baidu.ocr(img_path, latex=latex)
    else:
        ok, s = baidu.ocr(img_path, latex=latex)

    return ok, s


def check_server_translate(server, a, b):
    ok = False

    if (server == tools.server_tencent):
        ok = tencent.check(a, b)
    else:
        ok = baidu.check_translate(a, b)

    return ok


def check_server_ocr(server, a, b):
    ok = False

    if (server == tools.server_tencent):
        ok = tencent.check(a, b)
    else:
        ok = baidu.check_ocr(a, b)

    return ok
