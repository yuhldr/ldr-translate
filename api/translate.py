import os
from api.server import baidu
import config
import time

last_s = ""
last_s2 = "空白"
last_time = 0

path_next_s = "s_next"

# 整合一下，方便接入其他api接口


def text(s_from, fromLang="auto", type="baidu", add_old=True):
    global last_s, last_s2, last_time
    toLang, changeLang = get_to_language()

    # 文字和上次一样，并且被翻译的语言没有修改，就不翻译了
    if (last_s == s_from and not changeLang):
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


to_language_zh = ""
last_to_language_zh = ""


def set_to_language(to_lg):
    global to_language_zh
    to_language_zh = to_lg
    with open("data/toLang", "w") as file:
        file.write(to_lg)


def get_to_language():
    global to_language_zh, last_to_language_zh

    change_language = last_to_language_zh != to_language_zh

    file_path = "data/toLang"
    if (len(to_language_zh) == 0):
        if (os.path.exists(file_path)):
            with open(file_path, "r") as file:
                to_language_zh = file.read()
    if(len(to_language_zh) == 0):
        to_language_zh = config.translate_to_language_zh[0]
    print(last_to_language_zh + "==" + to_language_zh)
    last_to_language_zh = to_language_zh

    return to_language_zh, change_language
