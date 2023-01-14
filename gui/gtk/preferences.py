from api import translate
from api.server import baidu, tencent
from utils import config, version
from api.server_config import server_baidu, server_tencent, get_api_key
import threading


from gi.repository import Gtk, GLib


class Preference(Gtk.ApplicationWindow):

    def __init__(self, parent):
        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_default_size(400, 360)
        self.set_keep_above(True)
        self.set_title("翻译设置")
        self.set_icon_from_file('./icon/setting.svg')
        self.ind_parent = parent

        ui = Gtk.Builder()
        ui.add_from_file('./preference.ui')
        self.init_other(ui)
        self.init_baidu_api(ui)
        self.init_tencent(ui)
        self.add(ui.get_object('gd_prf'))
        self.show_all()

    def init_other(self, ui):

        cbtn_auto_start = ui.get_object('cbtn_auto_start')
        cbtn_auto_start.set_active(config.get_autostart())
        cbtn_auto_start.connect('toggled', self.update_autostart)

        cb_ocr_local = ui.get_object('cb_ocr_local')
        cb_ocr_local.set_active(config.is_ocr_local())
        cb_ocr_local.connect('toggled', self.update_ocr_local)

        self.lb_sys_msg = ui.get_object('lb_sys_msg')

        self.lb_version_msg = ui.get_object('lb_version_msg')

        self.lb_version_msg.set_markup(version.get_default())

        ui.get_object('btn_update').connect('clicked', self.check_update)

        self.cbb_tray_icon = ui.get_object('cbb_tray_icon')
        for tray_type in config.get_tray_types():
            self.cbb_tray_icon.append_text(tray_type)

        self.cbb_tray_icon.set_active(config.get_tray_icon_n())
        self.cbb_tray_icon.connect("changed", self.on_cbb_tray_icon)

    def on_cbb_tray_icon(self, combo):
        config.set_tray_icon(combo.get_active_text())

    def init_baidu_api(self, ui):

        def set_value(tv, key):
            tv.set_text(config.get_value(server_baidu, key))

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

        set_value(self.tv_baidu_translate_app_id, "translate_app_id")
        set_value(self.tv_baidu_translate_secret_key, "translate_secret_key")
        set_value(self.tv_baidu_ocr_app_key, "ocr_api_key")
        set_value(self.tv_baidu_ocr_secret_key, "ocr_secret_key")

        url_translate = "<a href='" + baidu.how_get_url_translate + "'>如何获取？</a>"
        url_ocr = "<a href='" + baidu.how_get_url_ocr + "'>如何获取？</a>"

        ui.get_object('lb_baidu_tanslate_way').set_markup(url_translate)
        ui.get_object('lb_baidu_ocr_way').set_markup(url_ocr)

    def init_tencent(self, ui):

        def set_value(tv, key):
            tv.set_text(config.get_value(server_tencent, key))

        self.tv_tencent_secret_id = ui.get_object('tv_tencent_secret_id')
        self.tv_tencent_secret_key = ui.get_object('tv_tencent_secret_key')
        self.lb_tencnet_msg = ui.get_object('lb_tencnet_msg')

        set_value(self.tv_tencent_secret_id, "translate_secret_id")
        set_value(self.tv_tencent_secret_key, "translate_secret_key")

        url = "<a href='" + tencent.how_get_url_translate + "'>如何获取？</a>"
        ui.get_object('lb_tencnet_way').set_markup(url)

        ui.get_object('btn_tencnet_save').connect("clicked", self.save_tencent)

    def save_baidu_translate(self, btn=None):

        self.save_server(
            self.tv_baidu_translate_app_id,
            self.tv_baidu_translate_secret_key,
            self.lb_baidu_translate_msg,
            server_baidu,
        )

    def save_baidu_ocr(self, btn=None):
        server = server_baidu

        config.set_config(server, "access_token", "")
        config.set_config(server, "expires_in_date", 0)

        self.save_server(self.tv_baidu_ocr_app_key,
                         self.tv_baidu_ocr_secret_key, self.lb_baidu_ocr_msg,
                         server, True)

    def save_tencent(self, btn=None):

        self.save_server(self.tv_tencent_secret_id, self.tv_tencent_secret_key,
                         self.lb_tencnet_msg, server_tencent)

    def get_text(self, text_view):
        tb = text_view.get_buffer()
        text = tb.get_text().strip()

        return text

    def update_autostart(self, menu_check):

        config.update_autostart(menu_check.get_active())

    def update_ocr_local(self, menu_check):
        config.set_ocr_local(menu_check.get_active())

    def check_update(self, view=None):

        def _check():
            s, msg = version.check_update()
            self.lb_version_msg.set_markup(s)

        self.lb_version_msg.set_markup("更新检查中……")

        tt = threading.Thread(target=_check)
        tt.start()

    def save_server(self, tv_a, tv_b, lb_msg, server, is_ocr=False):

        text_a = self.get_text(tv_a)
        text_b = self.get_text(tv_b)

        def _save(text_a, text_b):
            ok, text_a, text_b = translate.check_server_api(
                (is_ocr, server, text_a, text_b))

            msg = "超时或账号密码错误"

            tv_a.set_text(text_a)
            tv_b.set_text(text_b)

            if (ok):
                msg = "成功，已保存"
                key_a, key_b = get_api_key(server, is_ocr)
                config.set_config(server, key_a, text_a)
                config.set_config(server, key_b, text_b)
            lb_msg.set_text(msg)

        def _save_c(text_a, text_b):
            GLib.idle_add(_save, text_a, text_b)

        if (len(text_a) == 0 or len(text_b) == 0):
            lb_msg.set_text("已恢复默认（不推荐）")
        else:
            lb_msg.set_text("加载中...")
            tt = threading.Thread(target=_save_c, args=(
                text_a,
                text_b,
            ))
            tt.start()
