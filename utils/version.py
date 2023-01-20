import json

import requests

from utils import config

version_data = None


def get_value(key):
    global version_data
    if version_data is None:
        version_data = json.load(open("version.json", "r"))
    return version_data[key]


def check_update(qt=None):
    urls = get_value("urls")
    update = False
    i = 0
    while not update and i < len(urls):
        update, s, msg = check_update_version(urls[i])
        i += 1
    return s, msg


def get_default():
    version_version = get_value("name")
    version_code = get_value("code")
    version_home_url = get_value("home_url")

    return "<a href='%s'>当前版本：v%s.%d</a>" % (version_home_url, version_version,
                                                 version_code)


def check_update_version(url):
    update = False

    version_version = get_value("name")
    version_code = get_value("code")
    version_home_url = get_value("home_url")

    old_version_name = "v%s.%d" % (version_version, version_code)
    s = "<a href='%s'>请求错误，可以去看看，点我</a>" % version_home_url
    msg = ""

    try:
        request = requests.get(url, timeout=config.time_out)
        if request.status_code == 200:
            json_config = request.json()
            print(json_config)
            version_code_new = json_config["code"]
            update = version_code_new > version_code

            if update:
                s = "<a href='%s'>软件有更新：%s -> v%s.%d</a>" % (
                    json_config["home_url"], old_version_name,
                    json_config["name"], version_code_new)
            else:
                s = "<a href='%s'>暂无更新：%s</a>" % (version_home_url,
                                                      old_version_name)
    except Exception as e:
        print(e)
    print(s)
    return update, s, msg
