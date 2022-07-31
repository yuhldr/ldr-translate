server_baidu = "baidu"
server_tencent = "tencent"
server_youdao = "youdao"
server_google = "google"

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
        "auto": "auto",
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
