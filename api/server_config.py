server_baidu = "baidu"
server_tencent = "tencent"
server_youdao = "youdao"
server_google = "google"


def get_api_key(server, is_ocr=False):
    api_keys = dict_api_save[server]
    s = "t"
    if (is_ocr):
        s = "o"
    return api_keys[s + "a"], api_keys[s + "b"]


dict_api_save = {
    server_baidu: {
        "ta": "translate_app_id",
        "tb": "translate_secret_key",
        "oa": "ocr_api_key",
        "ob": "ocr_secret_key",
    },
    server_tencent: {
        "ta": "translate_secret_id",
        "tb": "translate_secret_key",
        "oa": "translate_secret_id",
        "ob": "translate_secret_key",
    },
}

dict_to_lang = {
    # 在locale/zh.json中对应的["translate"]["to_lang"]key：在此翻译服务中实际对应的toLang参数code
    server_baidu: {
        "auto": "auto",
        "zh": "zh",
        "wyw": "wyw",
        "en": "en",
        "jp": "jp",
        "kor": "kor",
        "de": "de",
        "fra": "fra",
    },
    server_google: {
        "zh": "zh",
        "en": "en",
        "jp": "ja",
        "kor": "ko",
        "de": "de",
        "fra": "fr",
    },
    server_tencent: {
        "zh": "zh",
        "en": "en",
        "jp": "jp",
        "kor": "kr",
        "de": "de",
        "fra": "fr",
    }
    # ,
    # server_youdao: {
    #     "zh": "zh",
    #     "en": "en"
    # }
}
