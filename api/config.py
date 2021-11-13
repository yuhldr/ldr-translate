import configparser
import json
import requests
from pathlib import Path

config = configparser.ConfigParser()
config_data = None
config_file_path = "config.json"


def load_configs():
    global config_data
    config_data = json.load(open(config_file_path, "r"))


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
    with open(config_file_path, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False)


# 更新时数据迁移
def old2new():

    old_config_file = "cache/" + config_file_path
    if Path(old_config_file).exists():
        config_data = json.load(open(old_config_file, "r"))

        for key in [
                "translate_app_id", "translate_secret_key", "ocr_api_key",
                "ocr_secret_key", "access_token", "expires_in_date"
        ]:
            set_config("baidu", key, config_data["baidu"][key])

        for key in ["translate_way_copy", "to_long"]:
            set_config("setting", key, config_data["setting"][key])
