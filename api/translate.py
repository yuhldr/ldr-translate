from api.server import baidu
import config
import time

last_s = ""
last_s2 = ""
last_time = 0

path_next_s = "s_next"

# 整合一下，方便接入其他api接口

def text(s_from,
         fromLang="auto",
         toLang=config.translate_to_language,
         type="baidu",
         add_old=True):
    global last_s, last_s2, last_time

    if (last_s == s_from):
        print("重复：    %s" % (s_from))
        return last_s, last_s2
    span = config.translate_span * 1.2 - (time.time() - last_time)
    if (span > 0):
        time.sleep(span)
    if (add_old):
        s_from = last_s + " " + s_from

    if (type == "baidu"):
        last_s2 = baidu.translate(s_from, fromLang, toLang)
    else:
        last_s2 = baidu.translate(s_from, fromLang, toLang)

    last_s = s_from
    last_time = time.time()
    return last_s, last_s2


def ocr(img, type="baidu"):

    if (type == "baidu"):
        s = baidu.ocr(img)
    else:
        s = baidu.ocr(img)

    return s
