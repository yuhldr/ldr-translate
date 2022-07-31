import requests
import json


version_data = None


def get_value(key):
    global version_data
    if(version_data is None):
        version_data = json.load(open("version.json", "r"))
    return version_data[key]


def check_update():
    urls = get_value("urls")
    update = False
    i = 0
    while not update and i < len(urls):
        update, s, msg = check_update_version(urls[i])
        i += 1
    return s, msg


def check_update_version(url):

    update = False

    version_version = get_value("name")
    version_code = get_value("code")
    version_home_url = get_value("home_url")

    old_version_name = "v%s.%d" % (version_version, version_code)
    s = "<a href='%s'>已是最新：%s</a>" % (version_home_url, old_version_name)
    msg = ""
    print(url)
    try:
        request = requests.get(url, timeout=2)
        if (request.status_code == 200):
            json_config = request.json()
            version_code_new = json_config["code"]
            update = version_code_new > version_code

            version_name = "v%s.%d" % (
                json_config["name"], version_code_new)
            if (update):
                s = "<a href='%s'>软件有更新：%s -> %s</a>" % (
                    json_config["home_url"],
                    old_version_name, version_name)

    except Exception as e:
        s = "<a href='%s'>软件有更新，点我</a>" % (version_home_url)
        print(e)

    return update, s, msg
