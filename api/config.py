import configparser
import json
import requests
import os
import shutil
from pathlib import Path

config = configparser.ConfigParser()
config_data = None
config_file_name = "config.json"
app_home_dir = os.getenv("HOME") + "/.cache/ldr-translate"
config_path = app_home_dir + "/" + config_file_name


def load_configs():
    global config_data
    config_data = json.load(open(config_path, "r"))


def get_update_version():
    update = False
    version_config_old = get_config_version()

    s = "关于：V " + version_config_old["name"]

    try:
        url = version_config_old["url"]
        request = requests.get(url)
        if (request.status_code == 200):
            json_config = request.json()
            update = json_config["version"]["code"] > version_config_old["code"]
            if (update):
                s = "软件有更新！"
    except Exception as e:
        print(e)

    return s, update


def get_config_section(section):
    if (config_data is None):
        load_configs()
    return config_data[section]


def get_config_setting():
    return get_config_section("setting")


def get_config_version():
    return get_config_section("version")


def get_translate_to_languages_zh():
    return get_config_setting()["translate_to_languages_zh"]


def set_config(section, key, value):
    global config_data
    if (config_data is None):
        load_configs()
    config_data[section][key] = value
    with open(config_path, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False)


# 更新时数据迁移
def old2new():
    print(config_path)
    if(os.path.exists(config_file_name)):
        config_data_new = json.load(open(config_file_name, "r"))
        if os.path.exists(config_path):
            print("旧文件已找到")
            config_data_old = json.load(open(config_path, "r"))
            api_servers = ["baidu"]
            for api_server in api_servers:
                for key in [
                        "translate_app_id", "translate_secret_key", "ocr_api_key",
                        "ocr_secret_key", "access_token", "expires_in_date"
                ]:
                    config_data_new[api_server][key] = config_data_old[api_server][key]

            for key in ["translate_way_copy", "to_long"]:
                config_data_new["setting"][key] = config_data_old["setting"][key]

        else:
            if not Path(app_home_dir).exists():
                os.makedirs(app_home_dir)

        with open(config_path, 'w') as file:
            json.dump(config_data_new, file, ensure_ascii=False)
        os.remove(config_file_name)

        print("数据迁移完毕")
