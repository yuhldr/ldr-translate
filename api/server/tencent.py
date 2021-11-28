import hashlib
import os
import random
import requests
import urllib
import time
import base64
import hmac
from urllib.parse import quote

from api import config, tools
import hmac

config_server = "tencent"
default_secret_id = "AKIDsiHacNr52j9IBpDJ8gyyh9LGuJSKvFI5"
default_secret_key = "XnmVx82f5E6h26tQhhQs3xaz80bw0pNV"
public_params = {}


def get_secret_id_key():
    config_baidu = config.get_config_section(config_server)

    secret_id = config_baidu["secret_id"]
    secret_key = config_baidu["secret_key"]

    if (len(secret_id) == 0 or len(secret_key) == 0):
        secret_id = default_secret_id
        secret_key = default_secret_key
    return secret_id, secret_key


def translate_text(s, fromLang="auto", toLangZh=""):
    config_baidu = config.get_config_section(config_server)

    secret_id, secret_key = get_secret_id_key()

    translate_to_languages = config_baidu["translate_to_languages"]

    # fromLang = "auto"   # 原文语种
    # toLang = "zh"   # 译文语种
    toLang = translate_to_languages[tools.to_lang_zh2par(toLangZh)]

    text, ok = translate(s, secret_id, secret_key, fromLang, toLang)
    return text


def translate(query_text,
              secret_id,
              secret_key,
              lang_from="auto",
              lang_to="zh",
              action="TextTranslate",
              endpoint="tmt.tencentcloudapi.com",
              query_method="GET",
              region="ap-beijing",
              version="2018-03-21"):
    ok = False
    data = {
        "Action": action,
        "Region": region,
        "SecretId": secret_id,
        "Timestamp": int(time.time()),
        "Nonce": random.randint(1, 1e6),
        "Version": version,
        "ProjectId": 0,
        "Source": lang_from,
        "SourceText": query_text,
        "Target": lang_to
    }
    s = get_string_to_sign(query_method, endpoint, data)
    print(s)
    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)
    print(data)
    try:
        request = requests.get("https://" + endpoint, params=data)
        print(request.text)
        if (request.status_code == 200):
            result = request.json()["Response"]
            if ("Error" in result):
                s1 = "腾讯翻译请求错误：" + result["Error"]["Code"] + " " + result[
                    "Error"]["Message"]
            else:
                ok = True
                s1 = result["TargetText"]
        else:
            s1 = "请求错误：" + request.content

    except Exception as e:
        s1 = "网络错误：" + str(e)

    return s1, ok


def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str


def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)


# TODO 有问题，以后再说
def ocr(img_path,
        latex=False,
        action="GeneralBasicOCR",
        endpoint="ocr.tencentcloudapi.com",
        query_method="GET",
        region="ap-beijing",
        version="2018-11-19"):
    secret_id, secret_key = get_secret_id_key()

    img_data = open(img_path, 'rb').read()

    img = base64.b64encode(img_data)
    print(img)
    ok = False
    data = {
        "Action": action,
        "Region": region,
        "SecretId": secret_id,
        "Timestamp": int(time.time()),
        "Nonce": random.randint(1, 1e6),
        "Version": version,
        "ImageBase64": img
    }

    s = get_string_to_sign(query_method, endpoint, data)

    data["Signature"] = sign_str(secret_key, s, hashlib.sha1)

    try:
        request = requests.get("https://" + endpoint, params=data)
        print(request.text)
        if (request.status_code == 200):
            result = request.json()["Response"]
            if ("Error" in result):
                s1 = "腾讯OCR请求错误：" + result["Error"]["Code"] + " " + result[
                    "Error"]["Message"]
            else:
                ok = True
                s1 = result["TargetText"]
        else:
            s1 = "请求错误：" + request.content

    except Exception as e:
        s1 = "网络错误：" + str(e)

    return ok, s1


def check(secret_id, secret_key):
    text, ok = translate("test", secret_id, secret_key, "auto", "zh")
    print(text)
    print(ok)

    return ok
