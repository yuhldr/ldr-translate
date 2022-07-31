from api import translate
from api.server import baidu, tencent
from utils import config, locale, version
from api import server_config

from gi.repository import Gtk
from preferences_sm import Preferences as PreferenceSM


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
        self.indicator_sysmonitor_preferences = None
        self.init_other(ui)
        self.init_baidu_api(ui)
        self.init_tencent(ui)
        self.add(ui.get_object('gd_prf'))
        self.show_all()
        show_sw = config.isShowSM()
        print(show_sw)
        self.cbtn_sys.set_active(show_sw)
        self.btn_set_sm.set_visible(show_sw)

    def init_other(self, ui):

        self.handler_id_show_sm = None

        version_home_url = version.get_value("home_url")
        version_name = version.get_value("name")
        version_code = version.get_value("code")
        print(version_name, version_code)

        cbtn_auto_start = ui.get_object('cbtn_auto_start')
        cbtn_auto_start.set_active(config.get_autostart())
        cbtn_auto_start.connect('toggled', self.update_autostart)

        self.btn_set_sm = ui.get_object('btn_set_sm')
        self.lb_sys_msg = ui.get_object('lb_sys_msg')

        self.handler_id_show_sm = self.btn_set_sm.connect(
            'clicked', self._on_indicator_sysmonitor_preferences)

        self.cbtn_sys = ui.get_object('cbtn_sys')
        self.cbtn_sys.connect('toggled', self.set_show_sm)

        self.lb_update_msg = ui.get_object('lb_update_msg')
        self.lb_version_msg = ui.get_object('lb_version_msg')

        self.lb_version_msg.set_markup(
            locale.get_locale_data("version", "msg"))
        self.lb_update_msg.set_markup(
            "<a href='%s'>当前版本：v%s.%d</a>" %
            (version_home_url, version_name, version_code))
        ui.get_object('lb_sm_github').set_markup(
            "<a href='https://github.com/fossfreedom/indicator-sysmonitor'>开源地址</a>"
        )

        ui.get_object('btn_update').connect('clicked', self.check_update)

    def init_baidu_api(self, ui):

        def set_value(tv, key):
            tv.set_text(config.get_value(server_config.server_baidu, key))

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

        print(url_translate)
        print(url_ocr)

        ui.get_object('lb_baidu_tanslate_way').set_markup(url_translate)
        ui.get_object('lb_baidu_ocr_way').set_markup(url_ocr)

    def init_tencent(self, ui):

        def set_value(tv, key):
            tv.set_text(config.get_value(server_config.server_tencent, key))

        self.tv_tencent_secret_id = ui.get_object('tv_tencent_secret_id')
        self.tv_tencent_secret_key = ui.get_object('tv_tencent_secret_key')
        self.lb_tencnet_msg = ui.get_object('lb_tencnet_msg')

        set_value(self.tv_tencent_secret_id, "translate_secret_id")
        set_value(self.tv_tencent_secret_key, "translate_secret_key")

        url = "<a href='" + tencent.how_get_url_translate + "'>如何获取？</a>"
        ui.get_object('lb_tencnet_way').set_markup(url)

        ui.get_object('btn_tencnet_save').connect("clicked", self.save_tencent)

    def save_baidu_translate(self, btn=None):

        ok = True
        server = "baidu"
        text_a = self.get_text(self.tv_baidu_translate_app_id)
        text_b = self.get_text(self.tv_baidu_translate_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok, a, b = translate.check_server_translate(server, text_a, text_b)
            self.tv_baidu_translate_app_id.set_text(a)
            self.tv_baidu_translate_secret_key.set_text(b)
            if (ok):
                msg = "成功，已保存"

        if (ok):
            config.set_config(server, "translate_app_id", a)
            config.set_config(server, "translate_secret_key", b)
        self.lb_baidu_translate_msg.set_text(msg)

    def save_baidu_ocr(self, btn=None):
        ok = True
        server = server_config.server_baidu

        text_a = self.get_text(self.tv_baidu_ocr_app_key)
        text_b = self.get_text(self.tv_baidu_ocr_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok, text_a, text_b = translate.check_server_ocr(
                server, text_a, text_b)
            self.tv_baidu_ocr_app_key.set_text(text_a)
            self.tv_baidu_ocr_secret_key.set_text(text_b)
            if (ok):
                msg = "成功，已保存"

        if (ok):
            config.set_config(server, "ocr_api_key", text_a)
            config.set_config(server, "ocr_secret_key", text_b)
            config.set_config(server, "access_token", "")
            config.set_config(server, "expires_in_date", 0)

        self.lb_baidu_ocr_msg.set_text(msg)

    def save_tencent(self, btn=None):
        ok = True
        server = server_config.server_tencent
        text_a = self.get_text(self.tv_tencent_secret_id)
        text_b = self.get_text(self.tv_tencent_secret_key)

        msg = "超时或账号密码错误"

        if (len(text_a) == 0 or len(text_b) == 0):
            msg = "已恢复默认（不推荐）"
        else:
            ok, text_a, text_b = translate.check_server_translate(
                server, text_a, text_b)
            self.tv_tencent_secret_id.set_text(text_a)
            self.tv_tencent_secret_key.set_text(text_b)
            if (ok):
                msg = "成功，已保存"

        if (ok):
            config.set_config(server, "translate_app_id", text_a)
            config.set_config(server, "translate_secret_key", text_b)
        self.lb_tencnet_msg.set_text(msg)

    def get_text(self, text_view):
        tb = text_view.get_buffer()
        text = tb.get_text().strip()

        return text

    def update_autostart(self, menu_check):
        print(menu_check.get_active())
        config.update_autostart(menu_check.get_active())

    def set_show_sm(self, menu_check):
        self.btn_set_sm.set_visible(menu_check.get_active())
        self.lb_sys_msg.set_markup("重新打开软件生效")
        print(menu_check.get_active())
        config.setShowSM(menu_check.get_active())

    def check_update(self, view=None):

        s, msg = version.check_update()

        self.lb_update_msg.set_markup(s)
        self.lb_version_msg.set_markup(msg)

    def _on_indicator_sysmonitor_preferences(self, event=None):
        if self.indicator_sysmonitor_preferences is not None:
            self._preferences_dialog.present()
            return

        self.indicator_sysmonitor_preferences = PreferenceSM(
            self, self.ind_parent)
        self.indicator_sysmonitor_preferences = None
