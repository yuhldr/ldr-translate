import gi
from api import config, translate

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Preference(Gtk.Window):
    server = "baidu"

    def __init__(self, title, server):
        Gtk.Window.__init__(self)

        self.server = server

        # self.set_default_size(450, 360)
        self.set_keep_above(True)

        ui = Gtk.Builder()
        ui.add_from_file('./ui/preference.ui')
        tc = ui.get_object('tc')

        self.hb = ui.get_object('pf_hb')
        self.hb.props.title = title
        self.set_titlebar(self.hb)

        self.tv_translate_app_id = ui.get_object('tv_translate_app_id')
        self.tv_translate_secret_key = ui.get_object('tv_translate_secret_key')
        self.lb_translate_msg = ui.get_object('lb_translate_msg')

        self.tv_ocr_app_key = ui.get_object('tv_ocr_app_key')
        self.tv_ocr_secret_key = ui.get_object('tv_ocr_secret_key')
        self.lb_ocr_msg = ui.get_object('lb_ocr_msg')

        config_baidu = config.get_config_section(self.server)

        self.tv_translate_app_id.get_buffer().set_text(config_baidu["translate_app_id"])
        self.tv_translate_secret_key.get_buffer().set_text(config_baidu["translate_secret_key"])
        self.tv_ocr_app_key.get_buffer().set_text(config_baidu["ocr_api_key"])
        self.tv_ocr_secret_key.get_buffer().set_text(config_baidu["ocr_secret_key"])

        ui.get_object('btn_translate_check').connect("clicked", self.check_translate)
        ui.get_object('btn_ocr_check').connect("clicked", self.check_ocr)
        ui.get_object('pf_save').connect("clicked", self.save)
        ui.get_object('pf_close').connect("clicked", self.close)

        url_translate = "<a href='" + config_baidu[
            "translate_url"] + "'>如何获取？</a>"
        url_ocr = "<a href='" + config_baidu["ocr_url"] + "'>如何获取？</a>"
        ui.get_object('lb_tanslate_way').set_markup(url_translate)
        ui.get_object('lb_ocr_way').set_markup(url_ocr)

        self.add(tc)
        self.show_all()

    def open(self):
        self.show_all()

    def close(self, a=None, b=None):
        self.destroy()

    def check_translate(self, btn=None, save=False):
        ok = False
        text_a = self.get_text(self.tv_translate_app_id)
        text_b = self.get_text(self.tv_translate_secret_key)

        msg = "超时或账号密码错误"

        if(len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok = translate.check_server_translate(self.server, text_a, text_b)
            if (ok):
                msg = "成功，已保存"
                config.set_config(self.server, "translate_app_id", text_a)
                config.set_config(self.server, "translate_secret_key", text_b)
        self.lb_translate_msg.set_text(msg)

        return ok, text_a, text_b

    def check_ocr(self, btn=None, save=False):
        ok = False
        text_a = self.get_text(self.tv_ocr_app_key)
        text_b = self.get_text(self.tv_ocr_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok = translate.check_server_ocr(self.server, text_a, text_b)
            if (ok):
                msg = "成功，已保存"
                config.set_config(self.server, "ocr_api_key", text_a)
                config.set_config(self.server, "ocr_secret_key", text_b)
                config.set_config(self.server, "access_token", "")
                config.set_config(self.server, "expires_in_date", 0)

        self.lb_ocr_msg.set_text(msg)

        return ok, text_a, text_b

    def get_text(self, text_view):
        tb = text_view.get_buffer()
        start_iter = tb.get_start_iter()
        end_iter = tb.get_end_iter()
        text = tb.get_text(start_iter, end_iter, True).strip()

        return text

    def save(self, a=None, b=None):
        self.check_translate(save=True)
        self.check_ocr(save=True)
