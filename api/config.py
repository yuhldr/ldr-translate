import json
import requests
import os
import shutil
from pathlib import Path

config_data = None
config_file_name = "config.json"

usr = os.getenv("SUDO_USER")
if (usr is None):
    usr = os.getenv("USER")

DESKTOP_NAME = "ldr-translate.desktop"
HOME_PATH = "/home/" + usr

DIR_CONFIG = HOME_PATH + "/.config"

AUTOSTART_DIR = DIR_CONFIG + '/autostart'
AUTOSTART_PATH = AUTOSTART_DIR + "/" + DESKTOP_NAME

app_home_dir = DIR_CONFIG + "/ldr-translate"
config_path = app_home_dir + "/" + config_file_name

DESKTOP_PATH = "/usr/share/applications/" + DESKTOP_NAME

print(AUTOSTART_PATH)


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
    "ocr_secret_key", "access_token", "expires_in_date", "translate_url", "ocr_url"
]
config_tencent_keys = ["secret_id", "secret_key", "url"]

config_setting_keys = ["translate_way_copy", "to_long", "server_name"]

config_sections_setting = "setting"
config_sections_version = "version"
config_sections_baidu = "baidu"
config_sections_tencent = "tencent"

# 超时时间不然会很卡
time_out = 2


def load_configs():
    check_config_data()
    global config_data
    config_data = json.load(open(config_path, "r"))
    print(get_config_version()["name"])


def check_update_version(url):

    update = False
    version_config_old = get_config_version()

    old_version_name = "v%s.%d" % (version_config_old["name"],
                                   version_config_old["code"])
    s = "<a href='%s'>已是最新：%s</a>" % (version_config_old["home_url"],
                                      old_version_name)
    msg = version_config_old["msg"]
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
                msg = json_config[config_sections_version]["msg"]
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
    with open(config_path, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False)


def check_dir(dir):
    if not Path(dir).exists():
        os.makedirs(dir)


def check_config_data():
    if (not os.path.exists(config_path)):
        check_dir(app_home_dir)
        if(os.path.exists(config_file_name)):
            shutil.copy(config_file_name, config_path)


# 更新时数据迁移，必须sudo执行
def old2new():
    print(config_path)
    if (os.path.exists(config_file_name)):
        config_data_new = json.load(open(config_file_name, "r"))
        if os.path.exists(config_path):
            print("旧文件已找到")
            config_data_old = json.load(open(config_path, "r"))

            # 百度
            for key in config_baidu_keys:
                config_data_new[config_sections_baidu][key] = config_data_old[
                    config_sections_baidu][key]

            # 腾讯
            for key in config_tencent_keys:
                config_data_new[config_sections_tencent][
                    key] = config_data_old[config_sections_tencent][key]

            for key in config_setting_keys:
                config_data_new[config_sections_setting][
                    key] = config_data_old[config_sections_setting][key]

        else:
            check_dir(app_home_dir)

        with open(config_path, 'w') as file:
            json.dump(config_data_new, file, ensure_ascii=False)

        print("数据迁移完毕")
