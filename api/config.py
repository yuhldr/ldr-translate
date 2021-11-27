import configparser
import json
import requests
import os
import shutil
from pathlib import Path

config = configparser.ConfigParser()
config_data = None
config_file_name = "config.json"
config_file_name_bak = "config.json_bak"
app_home_dir = os.getenv("HOME") + "/.cache/ldr-translate"
config_path = app_home_dir + "/" + config_file_name


def load_configs():
    global config_data
    config_data = json.load(open(config_path, "r"))


def check_update_version(url):
    print("更新：" + url)
    update = False
    version_config_old = get_config_version()

    old_version_name = "v%s.%d" % (version_config_old["name"], version_config_old["code"])
    s = "<a href='%s'>已是最新：v%s</a>" % (version_config_old["home_url"], old_version_name)
    msg = version_config_old["msg"]
    try:
        request = requests.get(url, timeout=2)
        if (request.status_code == 200):
            json_config = request.json()
            update = json_config["version"]["code"] > version_config_old["code"]

            version_name = "v%s.%d" % (json_config["version"]["name"],
                                       json_config["version"]["code"])
            if (update):
                s = "<a href='%s'>软件有更新：%s -> %s</a>" % (
                    json_config["version"]["home_url"], old_version_name,
                    version_name)
                msg = json_config["version"]["msg"]
    except Exception as e:
        print(e)

    return update, s, msg


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
        shutil.move(config_file_name, config_file_name_bak)

        print("数据迁移完毕")
    elif(not os.path.exists(config_path)):
        print("旧数据被删除了，恢复中……")

        if not Path(app_home_dir).exists():
            os.makedirs(app_home_dir)
        shutil.copy(config_file_name_bak, config_path)
