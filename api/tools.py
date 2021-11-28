from api import config

config_section = "setting"
to_language_zh = ""
last_to_language_zh = ""
translate_to_languages_zh = config.get_config_setting(
)["translate_to_languages_zh"]

last_server_name = ""
server_name = config.get_config_setting(
)["server_name"]


server_baidu = "baidu"
server_baidu_name = "百度"

server_tencent = "tencent"
server_tencent_name = "腾讯"

servers = {"百度": server_baidu, "腾讯": server_tencent}
servers_name = ["百度", "腾讯"]
# servers_name = ["百度"]


def set_server_name(name):
    global server_name
    server_name = name
    config.set_config(config_section, "server_name", server_name)


def get_server_():
    server_name, change_server = get_server_name_()
    return servers[server_name], change_server


def get_server():
    server, change_server = get_server_()
    return server


# 中文转为序号，与第三方对应
def server_par():
    return server_name2par(get_server_name())


def server_name2par(server_name):
    if (server_name is None or len(server_name) == 0):
        return 0
    print(servers_name)
    i = servers_name.index(server_name)
    if (i < 0):
        i = 0
    return i


def get_server_name():
    server_name, change_server = get_server_name_()
    return server_name


def get_server_name_():
    global server_name, last_server_name

    change_server = last_server_name != server_name

    server_name = config.get_config_setting()["server_name"]
    last_server_name = server_name

    return server_name, change_server


def set_to_lang_zh(to_lg):
    global to_language_zh
    to_language_zh = to_lg
    config.set_config(config_section, "to_long", to_lg)


def get_to_lang_zh():
    to_language_zh, change_language = get_to_lang_zh_()
    return to_language_zh


def get_to_lang_zh_():
    global to_language_zh, last_to_language_zh

    change_language = last_to_language_zh != to_language_zh

    to_language_zh = config.get_config_setting()["to_long"]
    last_to_language_zh = to_language_zh

    print("1 " + to_language_zh)

    return to_language_zh, change_language


# 中文转为序号，与第三方对应
def to_lang_zh2par(zh):
    if(zh is None or len(zh) == 0):
        return 0
    i = translate_to_languages_zh.index(zh)
    if (i < 0):
        i = 0
    return i


def to_lang_zh_par():
    return to_lang_zh2par(get_to_lang_zh())
