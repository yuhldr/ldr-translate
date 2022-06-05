#!/usr/bin/python3
# coding: utf-8
from api import translate, config, tools
from api.server import baidu

from gi.repository import Gtk, Gdk


class Translate(Gtk.ApplicationWindow):

    setting_titles = ["百度API", "其他待补充"]
    setting_title_types = [baidu.config_server, ""]
    is_hide = False
    isFirsts = [True, True, True]
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
        self.cbt_server.connect("changed", self.on_cbt_server_changed)
        for currency in tools.servers_name:
            self.cbt_server.append_text(currency)

        self.cbtn_add_old = ui.get_object('cbtn_add_old')
        # 公式识别
        self.cbtn_tex = ui.get_object('cbtn_tex')

        self.cbt_lang = ui.get_object('cbt_lang')
        self.cbt_lang.connect("changed", self.on_cbt_lang_changed)
        for currency in config.get_translate_to_languages_zh():
            self.cbt_lang.append_text(currency)

        ui.get_object('btn_translate').connect("clicked",
                                               self.update_translate_view)

        self.add(ui.get_object('box_translate'))
        self.connect("delete-event", self.close)

        # 初始化时载入上次的数据
        self.cbt_server.set_active(tools.server_par())
        self.cbt_lang.set_active(tools.to_lang_zh_par())
        self.clipboard = self.getClipboard()

    def copy_(self, a):
        translate.set_no_translate_this()

    def open(self):
        self.is_hide = False
        self.show_all()

    def close(self, a=None, b=None):
        self.is_hide = True
        self.destroy()

    def on_cbt_lang_changed(self, combo):
        text = combo.get_active_text()
        if text is None:
            text = config.get_translate_to_languages_zh()[0]
        tools.set_to_lang_zh(text)
        if (not self.isFirsts[1]):
            self.translate_by_s()
        else:
            self.isFirsts[1] = False
        return text

    def on_cbt_server_changed(self, combo):
        text = combo.get_active_text()
        if text is None:
            text = translate.servers_name[0]
        tools.set_server_name(text)
        if (not self.isFirsts[0]):
            self.translate_by_s()
        else:
            self.isFirsts[0] = False
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
        elif (not self.isFirsts[2]):
            ok, s_from = self.get_text_by_clipboard(self.clipboard)
            self.isFirsts[2] = False

        if (self.cbtn_tex.get_active()):
            if (s_from is None):
                s_from = "测试功能：\n勾选latex识别，可将图片公式转化为latex代码"
            self.set_text_view(s_from, "测试功能：\n勾选latex识别，可将图片公式转化为latex代码")
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

        if(len(s_from.strip()) > 0 and len(s_to.strip()) > 0):
            textbuffer_from.set_text(s_from.strip())
            textbuffer_to.set_text(s_to.strip())

    def getClipboard(self):
        if (config.get_config_setting()["translate_way_copy"]):
            return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        else:
            return Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
