import json
import os
import shutil
from pathlib import Path

config_data = None
config_file_name = "config.json"

HOME_PATH = os.getenv("SUDO_HOME")
if (HOME_PATH is None):
    HOME_PATH = os.getenv("HOME")

DESKTOP_NAME = "ldr-translate.desktop"

DIR_CONFIG = HOME_PATH + "/.config"

AUTOSTART_DIR = DIR_CONFIG + '/autostart'
AUTOSTART_PATH = AUTOSTART_DIR + "/" + DESKTOP_NAME

app_home_dir = DIR_CONFIG + "/ldr-translate"
config_home_path = app_home_dir + "/" + config_file_name
SETTINGS_FILE = app_home_dir + '/indicator-sysmonitor.json'

DESKTOP_PATH = "/usr/share/applications/" + DESKTOP_NAME

config_sections_setting = "setting"


def get_this_config_data():
    return json.load(open(config_file_name, "r"))


def get_config_data():
    global config_data
    if (config_data is None):
        if (not os.path.exists(config_home_path)):
            config_data = json.load(open(config_file_name, "r"))
        else:
            config_data = json.load(open(config_home_path, "r"))
    return config_data


def get_value(section, key):
    get_config_data()
    if (section not in config_data):
        return get_this_config_data()[section][key]
    if (key not in config_data[section]):
        return get_this_config_data()[section][key]
    return config_data[section][key]


def get_config_setting(key):
    return get_value(config_sections_setting, key)


def set_config(section, key, value):
    global config_data
    get_config_data()
    config_data[section][key] = value
    check_dir(app_home_dir)
    with open(config_home_path, 'w') as file:
        json.dump(config_data, file, ensure_ascii=False)


def check_dir(dir):
    if not Path(dir).exists():
        os.makedirs(dir)


# 显示网速等信息
def isShowSM():
    return get_config_setting("show_sm")


def setShowSM(b):
    return set_config(config_sections_setting, "show_sm", b)


# 开机自启
def update_autostart(autostart):
    if not autostart:
        try:
            os.remove(AUTOSTART_PATH)
        except Exception as e:
            print(e)
    else:
        try:
            if not os.path.exists(AUTOSTART_DIR):
                os.makedirs(AUTOSTART_DIR)
            shutil.copy(DESKTOP_PATH, AUTOSTART_PATH)
        except Exception as ex:
            print(ex)


def get_autostart():
    return os.path.exists(AUTOSTART_PATH)


# 超时时间不然会很卡
time_out = 2
