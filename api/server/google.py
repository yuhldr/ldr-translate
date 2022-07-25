import requests
import json


def translate_text(s, fromLang="auto", to_lang_code=""):
    print("谷歌" + to_lang_code)
    url = 'https://translate.google.cn/translate_a/single?'
    param = 'client=gtx&sl=%s&tl=%s&dt=t&q=%s' % (fromLang, to_lang_code, s)
    response = requests.get(url + param)
    result = json.loads(response.text)
    return result[0][0][0]


def get_Lang_dict():

    # 在locale.json中对应的key：这个翻译服务对应的简写
    return {
        "auto": "auto",
        "zh": "zh-cn",
        "en": "en",
        "jp": "ja",
        "kor": "ko",
        "de": "de",
        "fra": "fr",
    }
