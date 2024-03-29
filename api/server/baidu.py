import base64
import hashlib
import random
import time
import urllib

import requests

from api import server_config
from utils import locales, tools, config

config_server = server_config.server_baidu

how_get_url_translate = "https://doc.tern.1c7.me/zh/folder/setting/#%E7%99%BE%E5%BA%A6"
how_get_url_ocr = "https://cloud.baidu.com/doc/OCR/s/dk3iqnq51"

# 错误代码:locale文件中对应错误说明的key
error_msg2zh = {
    "54003": "error.t54003",
    "54000": "error.t54000",
    "54004": "error.t54004",
    "52001": "error.t52001",
    "52003": "error.t52003"
}

error_msg2zh_ocr = {
    "17": "error.o17",
    "110": "error.o110",
}


def translate_text(s, from_lang="auto", to_lang=""):
    app_id = config.get_value(config_server, "translate_app_id")
    secret_key = config.get_value(config_server, "translate_secret_key")

    if len(app_id) == 0 or len(secret_key) == 0:
        return locales.t_translate("baidu.error.t")

    text, ok = translate(s, app_id, secret_key, from_lang, to_lang)
    return text


def translate(s, app_id, secret_key, from_lang="auto", to_lang="zh"):
    ok = True

    salt = random.randint(32768, 65536)
    sign = app_id + s + str(salt) + secret_key
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = "https://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"
    url = url % (app_id, urllib.parse.quote(s), from_lang, to_lang, salt, sign)
    s1 = ""

    request = requests.get(url, timeout=config.time_out)
    result = request.json()

    if "error_code" in result:
        ok = False
        s1 = tools.error2zh(result["error_code"], result["error_msg"],
                            error_msg2zh, config_server)
    else:
        for trans_result in result["trans_result"]:
            s1 += trans_result["dst"] + "\n"

    return s1, ok


def get_token_by_url(ocr_api_key, ocr_secret_key):
    ok = False
    access_token = ""
    expires_in_date = -1

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ocr_api_key, ocr_secret_key)

    request = requests.get(host, timeout=config.time_out)

    jsons = request.json()
    if "access_token" not in jsons:
        access_token = "错误：" + jsons["error_description"]
    else:
        access_token = jsons["access_token"]
        expires_in_date = time.time() + jsons["expires_in"]
        ok = True

    return ok, str(access_token), expires_in_date


def get_token():
    ok = False
    access_token = ""

    expires_in_date = config.get_value(config_server, "expires_in_date")

    if expires_in_date - time.time() > 0:
        access_token = config.get_value(config_server, "access_token")
        if len(access_token) != 0:
            return True, access_token

    ocr_api_key = config.get_value(config_server, "ocr_api_key")
    ocr_secret_key = config.get_value(config_server, "ocr_secret_key")

    if len(ocr_api_key) == 0 or len(ocr_secret_key) == 0:
        return False, locales.t_translate("baidu.error.o")

    ok, access_token, expires_in_date = get_token_by_url(
        ocr_api_key, ocr_secret_key)
    if ok:
        config.set_config(config_server, "access_token", access_token)
        config.set_config(config_server, "expires_in_date", expires_in_date)

    return ok, access_token


def ocr(img_path):
    img_data = open(img_path, 'rb').read()
    # open('./images/lt.png', 'rb').read()
    '''
    通用文字识别
    '''
    s = ""
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/"

    request_url += "general_basic"

    img = base64.b64encode(img_data)
    ok, token = get_token()
    if not ok:
        return False, token
    params = {"image": img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url,
                             data=params,
                             headers=headers,
                             timeout=config.time_out)

    jsons = (response.json())

    if "error_code" in jsons:
        if 110 == jsons["error_code"]:
            config.set_config(config_server, "access_token", "")
        return False, tools.error2zh(jsons["error_code"], jsons["error_msg"],
                                     error_msg2zh_ocr, config_server)
    else:
        for word in jsons["words_result"]:
            s += word["words"] + '\n'

            s_ = word["words"]
            if s_[len(s_) - 1:len(s_)] != "-":
                s += " "

    return ok, s


def check_translate(appId, secretKey):
    text, ok = translate(
        "test",
        appId,
        secretKey,
        "auto",
        "zh",
    )
    return ok


def check_ocr(apiKey, secretKey):
    ok, access_token, expires_in_date = get_token_by_url(apiKey, secretKey)
    return ok
