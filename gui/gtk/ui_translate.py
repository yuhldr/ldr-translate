#!/usr/bin/python3
# coding: utf-8
from api import translate
from api.server import baidu
from utils import config, tools
from utils.locales import t_ui
from gi.repository import Gtk


class Translate(Gtk.ApplicationWindow):

    setting_titles = ["百度API", "其他待补充"]
    setting_title_types = [baidu.config_server, ""]
    is_hide = False
    clipboard = None

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_default_size(400, 360)
        self.set_icon_from_file('./icon/icon.svg')
        self.set_keep_above(True)
        self.set_title("兰译")

        ui = Gtk.Builder()
        ui.add_from_file('./translate.ui')

        self.tv_from = ui.get_object('tv_from')
        self.tv_to = ui.get_object('tv_to')

        self.tv_from.connect("copy-clipboard", self.copy_)
        self.tv_from.connect("cut-clipboard", self.copy_)
        self.tv_to.connect("copy-clipboard", self.copy_)
        self.tv_to.connect("cut-clipboard", self.copy_)

        self.cbt_server = ui.get_object('cbt_server')
        for currency in tools.get_translate_server_dict_by_locale().keys():
            self.cbt_server.append_text(currency)
        self.cbt_server.set_active(tools.get_current_translate_server_index())
        self.cbt_server.connect("changed", self.on_cbt_server_changed)

        self.cbtn_add_old = ui.get_object('cbtn_add_old')
        # 公式识别
        self.cbtn_tex = ui.get_object('cbtn_tex')

        self.cbt_lang = ui.get_object('cbt_lang')
        self.set_to_lang_data()
        self.cbt_lang.connect("changed", self.on_cbt_lang_changed)

        self.btn_translate = ui.get_object('btn_translate')
        self.btn_translate.connect("clicked", self.update_translate_view)

        self.add(ui.get_object('box_translate'))
        self.connect("delete-event", self.close)

        self.cbtn_add_old.set_label(t_ui("cb_add_label"))
        self.cbtn_tex.set_label(t_ui("cbtn_tex"))
        self.btn_translate.set_label(t_ui("btn_translate_label"))

    def copy_(self, a):
        translate.set_no_translate_this()

    def open(self):
        self.is_hide = False
        self.show_all()

    def close(self, a=None, b=None):
        self.is_hide = True
        self.destroy()

    def set_to_lang_data(self, i=-1):
        self.cbt_lang.remove_all()
        for currency in tools.get_to_lang_dict_by_locale().keys():
            self.cbt_lang.append_text(currency)

        if(i < 0):
            i = tools.get_current_to_lang_index()
        self.cbt_lang.set_active(i)

    def on_cbt_lang_changed(self, combo):
        text = combo.get_active_text()
        tools.set_to_lang(text)

        return text

    def on_cbt_server_changed(self, combo):
        text = combo.get_active_text()
        tools.set_translate_server(text)
        i = tools.get_current_to_lang_index(tools.translate_to_lang_cache)
        self.set_to_lang_data(i)

        return text

    def get_text_by_clipboard(self, clipboard_):
        text = ""
        ok = False
        image_pixbuf = clipboard_.wait_for_image()
        if image_pixbuf is not None:
            img_path = config.app_home_dir + "/copy_img"
            image_pixbuf.savev(img_path, "png", "", "")

            ok, text = translate.ocr(img_path,
                                     latex=self.cbtn_tex.get_active())
        else:
            text = clipboard_.wait_for_text()

        return ok, text

    def copy_auto_translate(self, clipboard_=None):
        s_from = None
        if (clipboard_ is not None):
            ok, s_from = self.get_text_by_clipboard(clipboard_)

        if (self.cbtn_tex.get_active()):
            if (s_from is None):
                s_from = t_ui("notice_from")
            self.set_text_view(s_from, t_ui("notice_to"))
        else:
            self.translate_by_s(s_from)

    # 按钮再次翻译（可能修改了文本）
    def update_translate_view(self, view=None):

        textbuffer_from = self.tv_from.get_buffer()

        start_iter = textbuffer_from.get_start_iter()
        end_iter = textbuffer_from.get_end_iter()
        s = textbuffer_from.get_text(start_iter, end_iter, True)

        self.translate_by_s(s_from=s)

    def translate_by_s(self, s_from=None):

        s_from, s_to = translate.text(s_from,
                                      add_old=self.cbtn_add_old.get_active())
        self.set_text_view(s_from, s_to)

    def set_text_view(self, s_from, s_to):

        textbuffer_from = self.tv_from.get_buffer()
        textbuffer_to = self.tv_to.get_buffer()

        if (len(s_from.strip()) > 0 and len(s_to.strip()) > 0):
            textbuffer_from.set_text(s_from.strip())
            textbuffer_to.set_text(s_to.strip())
