import json

import requests

from api import server_config
from utils import config

config_server = server_config.server_google


def translate_text(s, from_lang="auto", to_lang_code="zh-cn"):
    s = s.replace("#", "")
    print("谷歌" + to_lang_code)
    url = 'https://translate.googleapis.com/translate_a/single?'
    param = 'client=gtx&dt=t&sl=%s&tl=%s&q=%s' % (from_lang, to_lang_code, s)
    response = requests.get(url + param, timeout=config.time_out)
    result = json.loads(response.text)

    s = ""
    for ss in result[0]:
        s += ss[0]
    return s
