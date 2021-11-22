#!/usr/bin/python3
# coding: utf-8
from api import translate, config, tools
from api.server import baidu
from preferences import Preference

from gi.repository import Gtk, Gdk, Gio


class Translate(Gtk.ApplicationWindow):

    setting_titles = ["百度API", "其他待补充"]
    setting_title_types = [baidu.config_server, ""]
    is_hide = False
    isFirsts = [True, True]
    clipboard = None

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_default_size(400, 360)
        self.set_icon_from_file('./ui/icon.png')
        self.set_keep_above(True)

        ui = Gtk.Builder()
        ui.add_from_file('./ui/translate.ui')

        mbtn_prf = ui.get_object('mbtn_prf')
        menu = Gtk.Menu()
        mbtn_prf.set_popup(menu)
        for title in self.setting_titles:
            menuitem = Gtk.MenuItem(title)
            menuitem.connect("activate", self.on_menuitem_activated)
            menu.append(menuitem)
        menu.show_all()

        self.set_titlebar(ui.get_object('hb'))

        self.tv_from = ui.get_object('tv_from')
        self.tv_to = ui.get_object('tv_to')
        self.currency_combo = ui.get_object('currency_combo')
        self.cbtn_add_old = ui.get_object('cbtn_add_old')
        # 公式识别
        self.cbtn_tex = ui.get_object('cbtn_tex')
        self.sp_translate = ui.get_object('sp_translate')

        self.currency_combo.connect("changed", self.on_currency_combo_changed)
        for currency in config.get_translate_to_languages_zh():
            self.currency_combo.append_text(currency)

        ui.get_object('btn_translate').connect("clicked",
                                               self.update_translate_view)

        self.add(ui.get_object('box_translate'))
        self.connect("delete-event", self.close)

        # 初始化时载入上次的数据
        toLang, changeLang = tools.get_to_language()
        self.currency_combo.set_active(tools.zh2LangPar(toLang))
        self.clipboard = self.getClipboard()

    def open(self):
        self.is_hide = False
        self.show_all()

    def close(self, a=None, b=None):
        self.is_hide = True
        self.destroy()

    def on_menuitem_activated(self, menuitem):
        title = menuitem.get_label()
        i = self.setting_titles.index(title)
        window = Preference(title, self.setting_title_types[i])
        window.open()

    def on_currency_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is None:
            text = config.get_translate_to_languages_zh()[0]
        tools.set_to_language(text)
        if (not self.isFirsts[0]):
            self.translate_by_s()
        else:
            self.isFirsts[0] = False
        return text

    def get_text_by_clipboard(self, clipboard_):
        text = ""
        image_pixbuf = clipboard_.wait_for_image()
        if image_pixbuf is not None:
            img_path = config.app_home_dir + "/copy_img"
            image_pixbuf.savev(img_path, "png", "", "")

            text = translate.ocr(open(img_path, 'rb').read(),
                                    latex=self.cbtn_tex.get_active())
        else:
            text = clipboard_.wait_for_text()

        print(text)
        return text

    def copy_auto_translate(self, clipboard_=None):
        s_from = None
        self.sp_translate.start()
        if (clipboard_ is not None):
            s_from = self.get_text_by_clipboard(clipboard_)
        elif (not self.isFirsts[1]):
            s_from = self.get_text_by_clipboard(self.clipboard)
            self.isFirsts[1] = False

        if(self.cbtn_tex.get_active()):
            if(s_from is None):
                s_from = "测试功能：\n勾选latex识别，可将图片公式转化为latex代码"
            self.set_text_view(s_from, "测试功能：\n勾选latex识别，可将图片公式转化为latex代码")
        else:
            self.translate_by_s(s_from)

# 按钮再次翻译（可能修改了文本）
    def update_translate_view(self, view=None):
        self.sp_translate.start()

        textbuffer_from = self.tv_from.get_buffer()

        start_iter = textbuffer_from.get_start_iter()
        end_iter = textbuffer_from.get_end_iter()
        s = textbuffer_from.get_text(start_iter, end_iter, True)

        self.translate_by_s(s_from=s)

    def translate_by_s(self, s_from=None):

        s_from, s_to = translate.text(s_from, add_old=self.cbtn_add_old.get_active())
        self.set_text_view(s_from, s_to)

    def set_text_view(self, s_from, s_to):

        textbuffer_from = self.tv_from.get_buffer()
        textbuffer_to = self.tv_to.get_buffer()

        textbuffer_from.set_text(s_from.strip())
        textbuffer_to.set_text(s_to.strip())
        self.sp_translate.stop()

    def getClipboard(self):
        if (config.get_config_setting()["translate_way_copy"]):
            return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        else:
            return Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
