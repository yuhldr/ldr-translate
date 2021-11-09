#!/usr/bin/python3
# coding: utf-8

import gi
from api.translate import translate_data
import config

gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, Gdk


VERSION = '0.0.1'


class Translate(Gtk.Window):

    add_old = False

    def __init__(self):
        Gtk.Window.__init__(self)
        self._create_bar()
        self._create_content()
        self.set_icon_from_file('./ui/icon.png')
        self.connect("delete-event", Gtk.main_quit)
        self.set_keep_above(True)

        self.show_all()
        self.copy_translate()

    def close(self, a=None, b=None):
        self.hide()

    def _create_bar(self):

        # 定义HeaderBar
        hb = Gtk.HeaderBar()
        # 隐藏原有的工具按钮
        hb.set_show_close_button(False)
        hb.props.title = "兰译"
        self.set_titlebar(hb)

        btn_pin = Gtk.Button.new_with_label("追加×")
        # icon = Gio.ThemedIcon(name="view-pin-symbolic")
        # image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        # image = Gtk.Image.new_from_file("./ui/pin2.svg")
        # btn_pin.add(image)
        btn_pin.connect("clicked", self.set_add_old)
        hb.pack_start(btn_pin)

        btn_update = Gtk.Button.new_with_label("翻译")
        # icon = Gio.ThemedIcon(name="system-reboot-symbolic")
        # image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        # btn_update.add(image)
        btn_update.connect("clicked", self.update_translate_view)
        # 放置于HeaderBar右边
        hb.pack_end(btn_update)

    def _create_content(self):

        self.set_border_width(10)
        self.set_default_size(400, 360)

        self.box = Gtk.Box(spacing=18, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        self.scroll_from = Gtk.ScrolledWindow()
        self.text_view_from = Gtk.TextView()
        self.text_view_from.set_wrap_mode(wrap_mode=Gtk.WrapMode.CHAR)
        self.scroll_from.add(self.text_view_from)
        self.box.pack_start(self.scroll_from, True, True, 0)

        self.scroll_to = Gtk.ScrolledWindow()
        self.text_view_to = Gtk.TextView()
        self.text_view_to.set_wrap_mode(wrap_mode=Gtk.WrapMode.CHAR)
        self.scroll_to.add(self.text_view_to)
        self.box.pack_start(self.scroll_to, True, True, 0)

        # 选中即可，但是有时候会出现一些问题，因为选中期间，每次间断，都会回调
        # clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        # 复制以后才回调，比如快捷键复制、右键复制
        self.getClipboard().connect("owner-change", self.copy_auto_translate)

    def copy_auto_translate(self, cb, event=None):
        s_from = ""

        image = cb.wait_for_image()
        if image is not None:
            print(image.get_pixbuf())
        else:
            s_from = cb.wait_for_text()

        self.translate_by_s(s_from)

    def copy_translate(self, view=None):
        self.copy_auto_translate(cb=self.getClipboard())

    def update_translate_view(self, view=None):

        textbuffer_from = self.text_view_from.get_buffer()

        start_iter = textbuffer_from.get_start_iter()
        end_iter = textbuffer_from.get_end_iter()
        s = textbuffer_from.get_text(start_iter, end_iter, True)

        self.translate_by_s(s_from=s)

    def translate_by_s(self, s_from):

        textbuffer_from = self.text_view_from.get_buffer()
        textbuffer_to = self.text_view_to.get_buffer()

        if(s_from is None):
            s_from = "复制即可翻译"
            s_to = "Alt Q 快捷键、或状态栏图标可隐藏"
        else:
            s_from, s_to = translate_data(s_from.strip(), add_old=self.add_old)

        textbuffer_from.set_text(s_from.strip())
        textbuffer_to.set_text(s_to.strip())

    def getClipboard(self):
        if(config.translate_select):
            return Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        else:
            return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def set_add_old(self, view=None):
        self.add_old = not self.add_old
        if(self.add_old):
            view.set_label("追加√")
        else:
            view.set_label("追加×")


# win = Translate()

# Gtk.main()
