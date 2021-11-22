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


def translate_text(s, fromLang="auto", toLangZh=""):
    config_baidu = config.get_config_section(config_server)

    secret_id = config_baidu["secret_id"]
    secret_key = config_baidu["secret_key"]

    if (len(secret_id) == 0 or len(secret_key) == 0):
        secret_id = default_secret_id
        secret_key = default_secret_key

    translate_to_languages = config_baidu["translate_to_languages"]

    # fromLang = 'auto'   # 原文语种
    # toLang = 'zh'   # 译文语种
    toLang = translate_to_languages[tools.zh2LangPar(toLangZh)]

    text, ok = translate(s, secret_id, secret_key, fromLang, toLang)
    return text


def translate(
    query_text,
    secret_id,
    secret_key,
    lang_from="auto",
    lang_to="zh",
    action='TextTranslate',
    endpoint="tmt.tencentcloudapi.com",
):
    ok = False
    data = get_public_params(secret_id, secret_key, action, endpoint)
    data["ProjectId"] = 0
    data["Source"] = lang_from
    data["SourceText"] = query_text
    data["Target"] = lang_to
    print(data)
    try:
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            "Host": endpoint
        }

        request = requests.get("https://" + endpoint,
                               params=data,
                               headers=headers)
        print(request.text)
        if (request.status_code == 200):
            result = request.json()["Response"]
            if ("Error" in result):
                s1 = "腾讯翻译请求错误：" + result["Error"]["Code"] + " " + result[
                    "Error"]["Message"]
            else:
                ok = True
                s1 = result["Response"]["TargetText"]
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
    s = base64.b64encode(hmac_str)
    return str(s).split("'")[1]


def get_public_params(secret_id,
                      secret_key,
                      action,
                      endpoint,
                      query_method="GET",
                      region='ap-guangzhou',
                      version='2018-03-21'):

    global public_params
    if (action not in public_params):
        data = {
            'Action': 'DescribeInstances',
            'InstanceIds.0': 'ins-09dx96dg',
            'Limit': 20,
            'Nonce': 11886,
            'Offset': 0,
            'Region': 'ap-beijing',
            'SecretId': secret_id,
            'Timestamp': 1465185768,  # int(time.time())
            'Version': '2017-03-12'
        }
        data = {
            'Action': action,
            'Region': region,
            'SecretId': secret_id,
            'Timestamp': int(time.time()),
            "Nonce": random.randint(1, 1e6),
            'Version': version
        }
        s = get_string_to_sign(query_method, endpoint, data)
        data["Signature"] = sign_str(secret_key, s, hashlib.sha1)
        public_params[action] = data

    return public_params[action]


def tencent_get_url_encoded_params(secret_id, secret_key):
    action = 'TextTranslate'
    region = 'ap-guangzhou'
    timestamp = int(time.time())
    nonce = random.randint(1, 1e6)
    version = '2018-03-21'

    params_dict = {
        # 公共参数
        'Action': action,
        'Region': region,
        'Timestamp': timestamp,
        'Nonce': nonce,
        'SecretId': secret_id,
        'Version': version,
    }
    # 对参数排序，并拼接请求字符串
    params_str = ''
    for key in sorted(params_dict.keys()):
        pair = '='.join([key, str(params_dict[key])])
        params_str += pair + '&'
    params_str = params_str[:-1]
    # 拼接签名原文字符串
    signature_raw = 'GETtmt.tencentcloudapi.com/?' + params_str
    # 生成签名串，并进行url编码
    hmac_code = hmac.new(bytes(secret_key, 'utf8'),
                            signature_raw.encode('utf8'),
                            hashlib.sha1).digest()
    sign = quote(base64.b64encode(hmac_code))
    # 添加签名请求参数
    params_dict['Signature'] = sign
    # 将 dict 转换为 list 并拼接为字符串
    temp_list = []
    for k, v in params_dict.items():
        temp_list.append(str(k) + '=' + str(v))
    params_data = '&'.join(temp_list)
    return params_data

def tencent_parse(query_text):
    url_with_args = 'https://tmt.tencentcloudapi.com/?' + self.tencent_get_url_encoded_params(
        query_text)
    res = requests.get(url_with_args, headers=self.headers)
    json_res = res.json()
    trans_text = json_res['Response']['TargetText']
    return trans_text


def test():
    # s = translate_text("test")

    print(tencent_get_url_encoded_params(default_secret_id, default_secret_key))
    return None
