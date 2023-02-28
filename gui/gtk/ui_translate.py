#!/usr/bin/python3
# coding: utf-8
import threading
import time

from gi.repository import Gtk, GLib

from api import translate
from api.server import baidu
from utils import config, tools
from utils.locales import t_ui


def on_cbt_lang_changed(combo):
    text = combo.get_active_text()
    tools.set_to_lang(text)

    return text


def copy_(a):
    translate.set_no_translate_this()


class Translate(Gtk.ApplicationWindow):
    setting_titles = ["百度API", "其他待补充"]
    setting_title_types = [baidu.config_server, ""]
    is_hide = True
    clipboard = None
    deal_last = 0

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

        self.tv_from.connect("copy-clipboard", copy_)
        self.tv_from.connect("cut-clipboard", copy_)
        self.tv_to.connect("copy-clipboard", copy_)
        self.tv_to.connect("cut-clipboard", copy_)

        self.cbt_server = ui.get_object('cbt_server')
        for currency in tools.get_translate_server_dict_by_locale().keys():
            self.cbt_server.append_text(currency)
        self.cbt_server.set_active(tools.get_current_translate_server_index())
        self.cbt_server.connect("changed", self.on_cbt_server_changed)

        self.cbtn_add_old = ui.get_object('cbtn_add_old')

        self.cbt_lang = ui.get_object('cbt_lang')
        self.set_to_lang_data()
        self.cbt_lang.connect("changed", on_cbt_lang_changed)

        self.sp_translate = ui.get_object('sp_translate')
        self.btn_translate = ui.get_object('btn_translate')
        self.btn_translate.connect("clicked", self.update_translate_view)

        self.add(ui.get_object('box_translate'))
        self.connect("delete-event", self.close)

        self.cbtn_add_old.set_label(t_ui("cb_add_label"))

        self.btn_translate.set_label(t_ui("btn_translate_label"))

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

        if i < 0:
            i = tools.get_current_to_lang_index()
        self.cbt_lang.set_active(i)

    def on_cbt_server_changed(self, combo):
        text = combo.get_active_text()
        tools.set_translate_server(text)
        i = tools.get_current_to_lang_index(tools.translate_to_lang_cache)
        self.set_to_lang_data(i)

        return text

    def copy_auto_translate(self, clipboard=None):
        if clipboard is not None:
            span = time.time() - self.deal_last
            self.deal_last = time.time()
            if span < 0.5:
                return
            image = clipboard.wait_for_image()
            if image is not None:
                self.ocr_image(image)
            else:
                self.translate_by_s(clipboard.wait_for_text())
        else:
            self.set_text_view(t_ui("notice_from"), t_ui("notice_to"))

    # 按钮再次翻译（可能修改了文本）
    def update_translate_view(self, view=None):

        tb_from = self.tv_from.get_buffer()

        start_iter = tb_from.get_start_iter()
        end_iter = tb_from.get_end_iter()
        s = tb_from.get_text(start_iter, end_iter, True)

        self.translate_by_s(s_from=s)

    def ocr_image(self, image_p):

        def next_ocr(_img_path):
            ok, text = translate.ocr(_img_path)
            self.sp_translate.stop()
            self.translate_by_s(text)

        self.set_text_view(config.get_ocr_notice(), "识别中……")
        self.sp_translate.start()

        img_path = config.app_home_dir + "/copy_img"
        image_p.savev(img_path, "png", "", "")

        tt = threading.Thread(target=next_ocr,
                              args=(img_path,))
        tt.start()

    def translate_by_s(self, s_from=None):
        if translate.no_translate_this:
            translate.set_no_translate_this(False)
            return

        def request_text(s_from_=None):
            start_ = time.time()
            s_from_, s_to = translate.text(
                s_from_, add_old=self.cbtn_add_old.get_active())
            span = 0.5 - (time.time() - start_)
            if span > 0:
                time.sleep(span)
            self.set_text_view(s_from_, s_to)
            self.sp_translate.stop()

        if s_from is not None:
            self.set_text_view(s_from, "翻译中……")
            self.sp_translate.start()
        tt = threading.Thread(target=request_text, args=(s_from,))
        tt.start()

    def set_text_view(self, s_from, s_to):

        def set_text(s_from_, s_to_):
            if len(s_from_.strip()) > 0 and len(s_to_.strip()) > 0:
                self.tv_from.get_buffer().set_text(s_from_.strip())
                self.tv_to.get_buffer().set_text(s_to_.strip())

        GLib.idle_add(set_text, s_from, s_to)
