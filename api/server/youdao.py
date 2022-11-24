import requests
import urllib
from utils import config
from api import server_config

config_server = server_config.server_youdao


def translate_text(s, fromLang="auto", toLang=""):
    ok = True

    url = "http://fanyi.youdao.com/translate?&doctype=json&type=%s&i=%s"
    url = url % (fromLang + "2" + toLang, urllib.parse.quote(s))

    s1 = ""
    try:
        request = requests.get(url, timeout=config.time_out)
        if (request.status_code == 200):
            result = request.json()

            if ("errorCode" in result and result["errorCode"] != 0):
                ok = False
                s1 = "翻译错误,试试其他引擎?"
            else:
                print(result["translateResult"])
                for trans_result in result["translateResult"]:
                    s1 += trans_result[0]["tgt"] + "\n"
        else:
            s1 = "请求错误：" + request.content

    except Exception as e:
        print(e)
        s1 = "网络错误：" + str(e)

    return s1
