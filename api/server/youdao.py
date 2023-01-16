import urllib

import requests

from api import server_config
from utils import config

config_server = server_config.server_youdao


def translate_text(s, from_lang="auto", to_lang=""):
    ok = True

    url = "http://fanyi.youdao.com/translate?&doctype=json&type=%s&i=%s"
    url = url % (from_lang + "2" + to_lang, urllib.parse.quote(s))

    s1 = ""
    request = requests.get(url, timeout=config.time_out)
    if request.status_code == 200:
        result = request.json()

        if "errorCode" in result and result["errorCode"] != 0:
            ok = False
            s1 = "翻译错误,试试其他引擎?"
        else:
            print(result["translateResult"])
            for trans_result in result["translateResult"]:
                s1 += trans_result[0]["tgt"] + "\n"
    else:
        s1 = "请求错误：" + request.content

    return s1
