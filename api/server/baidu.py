import hashlib
import os
import random
import base64
import requests
import urllib
import config
import time


translate_to_language_baidu = [
    "zh",
    "wyw",
    "en",
    "jp",
    "kor",
    "de",
    "fra",
]


def translate(s, fromLang="auto", toLang=config.translate_to_language_zh[0]):

    appid = config.baidu_appid  # 填写你的appid
    secretKey = config.baidu_secretKey  # 填写你的密钥

    # fromLang = 'auto'   # 原文语种
    # toLang = 'zh'   # 译文语种
    i = config.translate_to_language_zh.index(toLang)
    print(toLang + " == " + str(i))
    toLang = translate_to_language_baidu[i]

    salt = random.randint(32768, 65536)
    sign = appid + s + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = "https://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"
    url = url % (appid, urllib.parse.quote(s), fromLang, toLang, salt, sign)
    try:
        request = requests.get(url)
        print(request.status_code)
        if(request.status_code == 200):
            result = request.json()
            print(result)
            if ("error_code" in result):
                s1 = "百度翻译请求错误：" + result["error_code"] + " " + result["error_msg"]
            else:
                s1 = result["trans_result"][0]["dst"]
        else:
            s1 = "请求错误：" + request.content

    except Exception as e:
        s1 = "网络错误：" + str(e)
    print(s1)

    return s1


# translate("this is apple")
def get_token(file_path="data/baidu_token"):
    access_token = ""
    if (os.path.exists(file_path)):
        with open(file_path, "r") as file:
            token = file.read()
            if(len(token) > 0 and token.find("|") > -1):
                max_date = token.split("|")[0]
                span = int(max_date) - time.time()
                print(span)
                if (span > 0):
                    access_token = token.split("|")[1]

        if(len(access_token) != 0):
            return access_token

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (config.baidu_ocr_api_key, config.baidu_ocr_secret_key)
    response = requests.get(host)
    if response:
        jsons = response.json()
        if ("error_code" in jsons):
            return jsons["error_description"]
        else:
            access_token = jsons["access_token"]
            with open(file_path, "w") as file:
                print("更新")
                date = time.time() + int(jsons["expires_in"])
                file.write("%d|%s" % (date, access_token))

    return access_token


def ocr(img_data):
    # open('./images/lt.png', 'rb').read()
    '''
    通用文字识别
    '''
    s = ""
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    img = base64.b64encode(img_data)
    token = get_token()
    params = {"image": img}
    request_url = request_url + "?access_token=" + token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        jsons = (response.json())
        print(jsons)
        if ("error_code" in jsons):
            return str(jsons["error_code"]) + jsons["error_msg"]
        else:
            for word in jsons["words_result"]:
                s += word["words"] + " "
    return s
