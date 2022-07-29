import json
import requests
import os
import shutil
from pathlib import Path

config_data = None
config_file_name = "config.json"
config_locale_file_name = "config_locale.json"

HOME_PATH = os.getenv("SUDO_HOME")
if (HOME_PATH is None):
    HOME_PATH = os.getenv("HOME")

DESKTOP_NAME = "ldr-translate.desktop"

DIR_CONFIG = HOME_PATH + "/.config"

AUTOSTART_DIR = DIR_CONFIG + '/autostart'
AUTOSTART_PATH = AUTOSTART_DIR + "/" + DESKTOP_NAME

app_home_dir = DIR_CONFIG + "/ldr-translate"
config_home_path = app_home_dir + "/" + config_file_name
config_locale_home_path = app_home_dir + "/" + config_locale_file_name
SETTINGS_FILE = app_home_dir + '/indicator-sysmonitor.json'

DESKTOP_PATH = "/usr/share/applications/" + DESKTOP_NAME

print(AUTOSTART_PATH)


def isShowSM():
    return get_config_setting()["show_sm"]


def setShowSM(b):
    return set_config(config_sections_setting, "show_sm", b)


def update_autostart(autostart):
    print(autostart)
    if not autostart:
        try:
            os.remove(AUTOSTART_PATH)
        except Exception as e:
            print(e)
    else:
        try:
            if not os.path.exists(AUTOSTART_DIR):
                os.makedirs(AUTOSTART_DIR)
            print(DESKTOP_PATH)
            print(AUTOSTART_PATH)
            shutil.copy(DESKTOP_PATH, AUTOSTART_PATH)
        except Exception as ex:
            print(ex)


def get_autostart():
    print(AUTOSTART_PATH)
    return os.path.exists(AUTOSTART_PATH)


config_baidu_keys = [
    "translate_app_id", "translate_secret_key", "ocr_api_key",
    "ocr_secret_key", "access_token", "expires_in_date"
]
config_tencent_keys = ["secret_id", "secret_key"]

config_setting_keys = [
    "translate_to_lang", "translate_server", "show_sm"
]

config_sections_setting = "setting"
config_sections_version = "version"

config_sections_baidu = "baidu"
config_sections_tencent = "tencent"
config_sections_youdao = "youdao"
config_sections_google = "google"

dict_to_lang = {
    # 在locale,json中对应的key：在此翻译服务中对应的toLang参数code
    config_sections_baidu: {
        "auto": "auto",
        "zh": "zh",
        "wyw": "wyw",
        "en": "en",
        "jp": "jp",
        "kor": "kor",
        "de": "de",
        "fra": "fra",
    },
    config_sections_google: {
        "zh": "zh",
        "en": "en",
        "jp": "ja",
        "kor": "ko",
        "de": "de",
        "fra": "fr",
    },
    config_sections_tencent: {
        "auto": "auto",
        "zh": "zh",
        "en": "en",
        "jp": "jp",
        "kor": "kr",
        "de": "de",
        "fra": "fr",
    }
    # ,
    # config_sections_youdao: {
    #     "zh": "zh",
    #     "en": "en"
    # }
}

# 超时时间不然会很卡
time_out = 2


def load_configs():
    check_config_data()
    global config_data
    config_data = json.load(open(config_home_path, "r"))
    print(config_data)
    print(get_config_version()["name"])


def check_update():
    urls = get_config_version()["url"]
    update = False
    i = 0
    while not update and i < len(urls):
        update, s, msg = check_update_version(urls[i])
        i += 1
    return s, msg


def check_update_version(url):

    update = False
    version_config_old = get_config_version()

    old_version_name = "v%s.%d" % (version_config_old["name"],
                                   version_config_old["code"])
    s = "<a href='%s'>已是最新：%s</a>" % (version_config_old["home_url"],
                                      old_version_name)
    msg = ""
    try:
        request = requests.get(url, timeout=time_out)
        if (request.status_code == 200):
            json_config = request.json()
            update = json_config[config_sections_version][
                "code"] > version_config_old["code"]

            version_name = "v%s.%d" % (
                json_config[config_sections_version]["name"],
                json_config[config_sections_version]["code"])
            if (update):
                s = "<a href='%s'>软件有更新：%s -> %s</a>" % (
                    json_config[config_sections_version]["home_url"],
                    old_version_name, version_name)

    except Exception as e:
        print(e)

    print(s)
    print(update)
    return update, s, msg


def get_config_section(section):
    if (config_data is None):
        load_configs()
    return config_data[section]


def get_config_setting():
    return get_config_section(config_sections_setting)


def get_config_version():
    return get_config_section(config_sections_version)


def get_translate_to_languages_zh():
    return get_config_setting()["translate_to_languages_zh"]


def set_config(section, key, value):
    global config_data
    if (config_data is None):
        load_configs()
    config_data[section][key] = value
    with open(config_home_path, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False)


def check_dir(dir):
    if not Path(dir).exists():
        os.makedirs(dir)


def check_config_data():
    if (not os.path.exists(config_home_path)):
        check_dir(app_home_dir)
        if (os.path.exists(config_file_name)):
            shutil.copy(config_file_name, config_home_path)


# 更新时数据迁移，必须sudo执行
def old2new():
    print("准备迁移")
    check_dir(app_home_dir)

    shutil.copy(config_locale_file_name, config_locale_home_path)

    if (os.path.exists(config_file_name)):
        config_data_new = json.load(open(config_file_name, "r"))
        if os.path.exists(config_home_path):
            print("旧文件已找到")
            config_data_old = json.load(open(config_home_path, "r"))

            # 百度
            for key in config_baidu_keys:
                if (key in config_data_old[config_sections_baidu]):
                    config_data_new[config_sections_baidu][key] = \
                        config_data_old[config_sections_baidu][key]

            # 腾讯
            for key in config_tencent_keys:
                if (key in config_data_old[config_sections_tencent]):
                    config_data_new[config_sections_tencent][
                        key] = config_data_old[config_sections_tencent][key]

            for key in config_setting_keys:
                if (key in config_data_old[config_sections_setting]):
                    config_data_new[config_sections_setting][
                        key] = config_data_old[config_sections_setting][key]

        else:
            print("没有旧文件？")
            check_dir(app_home_dir)

        with open(config_home_path, 'w') as file:
            json.dump(config_data_new, file, ensure_ascii=False)

        print("数据迁移完毕")
