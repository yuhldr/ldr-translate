import requests
import json
from api import server_config


config_server = server_config.server_google


def translate_text(s, fromLang="auto", to_lang_code="zh-cn"):
    s = s.replace("#", "")
    print("谷歌" + to_lang_code)
    url = 'https://translate.googleapis.com/translate_a/single?'
    param = 'client=gtx&dt=t&sl=%s&tl=%s&q=%s' % (fromLang, to_lang_code, s)
    response = requests.get(url + param)
    result = json.loads(response.text)

    s = ""
    for ss in result[0]:
        s += ss[0]
    return s
