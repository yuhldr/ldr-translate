import gi
from api import config, translate, tools

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Preference(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_default_size(400, 360)
        self.set_keep_above(True)
        self.set_title("翻译设置")

        ui = Gtk.Builder()
        ui.add_from_file('./preference.ui')

        self.init_other(ui)
        self.init_baidu_api(ui)
        self.init_tencent(ui)
        self.add(ui.get_object('gd_prf'))
        self.show_all()

    def init_other(self, ui):

        config_version = config.get_config_version()

        cbtn_auto_start = ui.get_object('cbtn_auto_start')
        cbtn_auto_start.set_active(config.get_autostart())
        cbtn_auto_start.connect('toggled', self.update_autostart)

        self.lb_update_msg = ui.get_object('lb_update_msg')
        self.lb_version_msg = ui.get_object('lb_version_msg')

        self.lb_version_msg.set_markup(config_version["msg"])
        self.lb_update_msg.set_markup(
            "<a href='%s'>当前版本：v%s.%d</a>" %
            (config_version["home_url"], config_version["name"],
             config_version["code"]))

        ui.get_object('btn_update').connect('clicked', self.check_update)

    def init_baidu_api(self, ui):

        self.tv_baidu_translate_app_id = ui.get_object(
            'tv_baidu_translate_app_id')
        self.tv_baidu_translate_secret_key = ui.get_object(
            'tv_baidu_translate_secret_key')
        self.lb_baidu_translate_msg = ui.get_object('lb_baidu_translate_msg')

        self.tv_baidu_ocr_app_key = ui.get_object('tv_baidu_ocr_app_key')
        self.tv_baidu_ocr_secret_key = ui.get_object('tv_baidu_ocr_secret_key')
        self.lb_baidu_ocr_msg = ui.get_object('lb_baidu_ocr_msg')

        ui.get_object('btn_baidu_translate_save').connect(
            "clicked", self.save_baidu_translate)
        ui.get_object('btn_baidu_ocr_save').connect("clicked",
                                                    self.save_baidu_ocr)
        config_api = config.get_config_section(tools.server_baidu)

        self.tv_baidu_translate_app_id.get_buffer().set_text(
            config_api["translate_app_id"])
        self.tv_baidu_translate_secret_key.get_buffer().set_text(
            config_api["translate_secret_key"])
        self.tv_baidu_ocr_app_key.get_buffer().set_text(
            config_api["ocr_api_key"])
        self.tv_baidu_ocr_secret_key.get_buffer().set_text(
            config_api["ocr_secret_key"])

        url_translate = "<a href='" + config_api[
            "translate_url"] + "'>如何获取？</a>"
        url_ocr = "<a href='" + config_api["ocr_url"] + "'>如何获取？</a>"
        ui.get_object('lb_baidu_tanslate_way').set_markup(url_translate)
        ui.get_object('lb_baidu_ocr_way').set_markup(url_ocr)

    def init_tencent(self, ui):

        self.tv_tencent_secret_id = ui.get_object('tv_tencent_secret_id')
        self.tv_tencent_secret_key = ui.get_object('tv_tencent_secret_key')
        self.lb_tencnet_msg = ui.get_object('lb_tencnet_msg')

        config_api = config.get_config_section(tools.server_tencent)
        url = "<a href='" + config_api["url"] + "'>如何获取？</a>"
        ui.get_object('lb_tencnet_way').set_markup(url)

        ui.get_object('btn_tencnet_save').connect("clicked", self.save_tencent)

    def save_baidu_translate(self, btn=None):

        ok = False
        server = "baidu"
        text_a = self.get_text(self.tv_baidu_translate_app_id)
        text_b = self.get_text(self.tv_baidu_translate_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok = translate.check_server_translate(server, text_a, text_b)
            if (ok):
                msg = "成功，已保存"
                config.set_config(server, "translate_app_id", text_a)
                config.set_config(server, "translate_secret_key", text_b)
        self.lb_baidu_translate_msg.set_text(msg)

    def save_baidu_ocr(self, btn=None):
        ok = False
        server = tools.server_baidu

        text_a = self.get_text(self.tv_baidu_ocr_app_key)
        text_b = self.get_text(self.tv_baidu_ocr_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok = translate.check_server_ocr(server, text_a, text_b)
            if (ok):
                msg = "成功，已保存"
                config.set_config(server, "ocr_api_key", text_a)
                config.set_config(server, "ocr_secret_key", text_b)
                config.set_config(server, "access_token", "")
                config.set_config(server, "expires_in_date", 0)

        self.lb_baidu_ocr_msg.set_text(msg)

    def save_tencent(self, btn=None):
        ok = False
        server = tools.server_tencent
        text_a = self.get_text(self.tv_tencent_secret_id)
        text_b = self.get_text(self.tv_tencent_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok = translate.check_server_translate(server, text_a, text_b)
            if (ok):
                msg = "成功，已保存"
                config.set_config(server, "translate_app_id", text_a)
                config.set_config(server, "translate_secret_key", text_b)
        self.lb_tencnet_msg.set_text(msg)

    def get_text(self, text_view):
        tb = text_view.get_buffer()
        start_iter = tb.get_start_iter()
        end_iter = tb.get_end_iter()
        text = tb.get_text(start_iter, end_iter, True).strip()

        return text

    def update_autostart(self, menu_check):
        print(menu_check.get_active())
        config.update_autostart(menu_check.get_active())

    def check_update(self, view=None):
        urls = [
            "https://raw.githubusercontent.com/yuhldr/ldr-translate/master/config.json",
            "https://gitee.com/yuhldr/ldr-translate/raw/master/config.json",
            config.get_config_version()["url"]
        ]
        update = False
        i = 0
        while not update and i < len(urls):
            update, s, msg = config.check_update_version(urls[i])
            i += 1

        self.lb_update_msg.set_markup(s)
        self.lb_version_msg.set_markup(msg)
