import hashlib
import random
import base64
import requests
import urllib
import time
from api import config, tools

config_server = "baidu"
default_translate_app_id = "20211109000995303"
default_translate_secret_key = "qLFDFx7fLRrioaa6CTnk"
default_ocr_app_key = "S1NHCzzzBhL2TUMx5iGpOSUu"
default_ocr_secret_key = "709INHX6GCLsAXXZPLhKGVMmra7bEwGl"

error_msg2zh = {
    "54003": "百度翻译公钥使用人数过多，可重试。但建议在设置中，更换为自己的api密钥（可免费申请，更安全）",
    "54000": "翻译内容为空",
}

error_msg2zh_ocr = {
    "17": "图片识别公钥使用人数过多，下个月才可使用。建议在设置中，更换为自己的api密钥（可免费申请，更安全，额度更多）",
    "110": "意外错误，请重试",
}


def translate_text(s, fromLang="auto", toLangZh=""):
    config_baidu = config.get_config_section(config_server)

    appId = config_baidu["translate_app_id"]
    secretKey = config_baidu["translate_secret_key"]

    if (len(appId) == 0 or len(secretKey) == 0):
        appId = default_translate_app_id
        secretKey = default_translate_secret_key

    translate_to_languages = config_baidu["translate_to_languages"]

    # fromLang = 'auto'   # 原文语种
    # toLang = 'zh'   # 译文语种
    toLang = translate_to_languages[tools.to_lang_zh2par(toLangZh)]

    text, ok = translate(s, appId, secretKey, fromLang, toLang)
    return text


def translate(s, appId, secretKey, fromLang="auto", toLang="zh"):
    ok = True

    salt = random.randint(32768, 65536)
    sign = appId + s + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = "https://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"
    url = url % (appId, urllib.parse.quote(s), fromLang, toLang, salt, sign)
    try:
        request = requests.get(url, timeout=config.time_out)
        if (request.status_code == 200):
            result = request.json()
            if ("error_code" in result):
                s1 = tools.error2zh(result["error_code"], result["error_msg"],
                                    error_msg2zh)
            else:
                s1 = result["trans_result"][0]["dst"]
        else:
            s1 = "请求错误：" + request.content

    except Exception as e:
        s1 = "网络错误：" + str(e)

    return s1, ok


def get_token_by_url(ocr_api_key, ocr_secret_key):
    ok = False
    access_token = ""
    expires_in_date = -1

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ocr_api_key, ocr_secret_key)
    try:
        request = requests.get(host, timeout=config.time_out)

        jsons = request.json()
        if ("access_token" not in jsons):
            access_token = "错误：" + jsons["error_description"]
        else:
            access_token = jsons["access_token"]
            expires_in_date = time.time() + jsons["expires_in"]
            ok = True

    except Exception as e:
        access_token = "请求错误：" + str(e)

    return ok, str(access_token), expires_in_date


def get_token():
    ok = False
    access_token = ""

    config_baidu = config.get_config_section(config_server)
    expires_in_date = config_baidu["expires_in_date"]

    if (expires_in_date - time.time() > 0):
        access_token = config_baidu["access_token"]
        if (len(access_token) != 0):
            return True, access_token

    ocr_api_key = config_baidu["ocr_api_key"]
    ocr_secret_key = config_baidu["ocr_secret_key"]

    if (len(ocr_api_key) == 0 or len(ocr_secret_key) == 0):
        ocr_api_key = default_ocr_app_key
        ocr_secret_key = default_ocr_secret_key

    ok, access_token, expires_in_date = get_token_by_url(
        ocr_api_key, ocr_secret_key)
    if (ok):
        config.set_config(config_server, "access_token", access_token)
        config.set_config(config_server, "expires_in_date", expires_in_date)

    return ok, access_token


def ocr(img_path, latex=False):
    img_data = open(img_path, 'rb').read()
    # open('./images/lt.png', 'rb').read()
    '''
    通用文字识别
    '''
    s = ""
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/"
    if (latex):
        request_url += "formula"
    else:
        request_url += "general_basic"

    img = base64.b64encode(img_data)
    ok, token = get_token()
    params = {"image": img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url,
                             data=params,
                             headers=headers,
                             timeout=config.time_out)

    if response:
        jsons = (response.json())

        if ("error_code" in jsons):
            if(110 == jsons["error_code"]):
                config.set_config(config_server, "access_token", "")
            return False, tools.error2zh(jsons["error_code"],
                                         jsons["error_msg"], error_msg2zh_ocr)
        else:
            for word in jsons["words_result"]:
                s += word["words"]
                if (latex):
                    s += "\n"
                else:
                    s_ = word["words"]
                    if (s_[len(s_) - 1:len(s_)] != "-"):
                        s += " "

    else:
        print(response.text)

    if (latex):
        s = s.replace(" _ ", "_")
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
