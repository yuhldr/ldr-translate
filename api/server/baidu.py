import hashlib
import random
import json
import requests
import urllib
import config

def translate(s, fromLang="auto", toLang='zh'):

    appid = config.baidu_appid  # 填写你的appid
    secretKey = config.baidu_secretKey  # 填写你的密钥

    # fromLang = 'auto'   # 原文语种
    # toLang = 'zh'   # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + s + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = "https://api.fanyi.baidu.com/api/trans/vip/translate?appid=%s&q=%s&from=%s&to=%s&salt=%s&sign=%s"
    url = url % (appid, urllib.parse.quote(s), fromLang, toLang, salt, sign)
    try:
        request = requests.get(url)
        print(request.status_code)
        if(request.status_code == 200):
            result = json.loads(request.text)
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
